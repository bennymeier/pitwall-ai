"""OpenAI Responses API orchestration."""

import json
from typing import Any

from pitwall_ai.api.jolpica_client import JolpicaClient
from pitwall_ai.assistant import tools as tool_impl
from pitwall_ai.assistant.tool_registry import TOOLS
from pitwall_ai.config import Settings
from pitwall_ai.prompts import BASELINE_PROMPT, SYSTEM_PROMPT
from pitwall_ai.rag.vector_store import VectorStore


class AssistantService:
    """Generate German answers using baseline or hybrid routing."""

    def __init__(
        self,
        settings: Settings,
        client: JolpicaClient,
        store: VectorStore,
        openai_client: Any = None,
    ) -> None:
        """Initialize the service with injectable dependencies."""
        self.settings = settings
        self.client = client
        self.store = store
        self.openai_client = openai_client
        self.last_tool_results: list[tuple[str, Any]] = []

    def answer(self, question: str, mode: str = "Hybrid") -> tuple[str, list[str]]:
        """Answer one question and return answer text plus used tool names."""
        self.last_tool_results = []
        if not question.strip():
            return "Bitte stelle eine konkrete Formel-1-Frage.", []
        if self.openai_client is None or not self.settings.openai_model:
            return (
                "OpenAI ist nicht konfiguriert. Setze OPENAI_API_KEY und OPENAI_MODEL.",
                [],
            )
        response = self.openai_client.responses.create(
            model=self.settings.openai_model,
            instructions=BASELINE_PROMPT if mode == "Baseline" else SYSTEM_PROMPT,
            input=question,
            tools=[] if mode == "Baseline" else TOOLS,
        )
        used: list[str] = []
        # In hybrid mode, execute requested tools until the model returns a final answer.
        while True:
            function_calls = [
                item
                for item in getattr(response, "output", [])
                if getattr(item, "type", "") == "function_call"
            ]
            if not function_calls:
                break
            tool_outputs: list[dict[str, str]] = []
            for item in function_calls:
                name = str(item.name)
                arguments = json.loads(item.arguments)
                result = self._call_tool(name, arguments)
                used.append(name)
                self.last_tool_results.append((name, result))
                # The response ID links these results to the model's pending function calls.
                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result.model_dump_json(),
                    }
                )
            response = self.openai_client.responses.create(
                model=self.settings.openai_model,
                instructions=SYSTEM_PROMPT,
                previous_response_id=response.id,
                input=tool_outputs,
                tools=TOOLS,
            )
        return getattr(response, "output_text", "Die Antwort konnte nicht erzeugt werden."), used

    def _call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Dispatch only registered model tools."""
        mapping = {
            "get_season_schedule": lambda: tool_impl.get_season_schedule(self.client, **arguments),
            "get_race_results": lambda: tool_impl.get_race_results(self.client, **arguments),
            "get_driver_standings": lambda: tool_impl.get_driver_standings(
                self.client, **arguments
            ),
            "get_constructor_standings": lambda: tool_impl.get_constructor_standings(
                self.client, **arguments
            ),
            "get_circuit_information": lambda: tool_impl.get_circuit_information(
                self.client, **arguments
            ),
            "get_driver_information": lambda: tool_impl.get_driver_information(
                self.client, **arguments
            ),
            "get_constructor_information": lambda: tool_impl.get_constructor_information(
                self.client, **arguments
            ),
            "get_driver_season_results": lambda: tool_impl.get_driver_season_results(
                self.client, **arguments
            ),
            "compare_drivers": lambda: tool_impl.compare_drivers(self.client, **arguments),
            "search_knowledge_base": lambda: tool_impl.search_knowledge_base(
                self.store, **arguments
            ),
        }
        if name not in mapping:
            raise ValueError(f"Unknown tool: {name}")
        return mapping[name]()
