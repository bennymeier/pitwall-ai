"""Streamlit chat interface."""

import random
from typing import Any

import streamlit as st
from openai import OpenAI

from pitwall_ai.api.jolpica_client import JolpicaClient
from pitwall_ai.assistant.service import AssistantService
from pitwall_ai.config import Settings, get_settings
from pitwall_ai.rag.vector_store import VectorStore

EXAMPLE_QUESTIONS = [
    "Wer gewann den Großen Preis von Monaco 2024?",
    "Was ist der Unterschied zwischen Fahrer- und Konstrukteurswertung?",
    "Welcher Fahrer hat die meisten Weltmeistertitel gewonnen?",
    "Wie funktioniert das Punktesystem in der Formel 1?",
    "Welche Teams fahren in der Saison 2024?",
    "Was bedeutet ein Safety Car für das Rennen?",
    "Wer gewann den Großen Preis von Silverstone 2023?",
    "Warum ist Monaco trotz weniger Überholmöglichkeiten so berühmt?",
    "Wie entscheidet ein Team zwischen einem und zwei Boxenstopps?",
    "Was ist der Unterschied zwischen Medium-, Soft- und Hard-Reifen?",
    "Welche Rolle spielt der Windkanal bei der Entwicklung eines F1-Autos?",
    "Was passiert bei einer roten Flagge während des Rennens?",
    "Wie hat sich die Formel 1 seit der Einführung des Ground Effect verändert?",
    "Welche Fahrerduelle gehören zu den spannendsten der F1-Geschichte?",
    "Welches Rennen gilt als eines der dramatischsten Formel-1-Finals?",
    "Wie funktioniert ein Undercut in der Formel 1?",
    "Warum sind Stadtkurse für Fahrer und Teams besonders anspruchsvoll?",
    "Welche Faktoren entscheiden über die Pole Position im Qualifying?",
    "Wie unterscheiden sich Ferrari, Mercedes und Red Bull bei ihrer Rennstrategie?",
]

CHART_EXAMPLE_QUESTIONS = [
    "Stelle die Fahrerwertung 2024 als Balkendiagramm dar.",
    "Stelle die Konstrukteurswertung 2024 als Balkendiagramm dar.",
    "Vergleiche die Gesamtpunkte von Lewis Hamilton und Max Verstappen von 2021 bis 2024 in einem Diagramm.",
]


def run() -> None:
    """Render the interactive German assistant."""
    settings = get_settings()
    st.set_page_config(page_title="Pitwall AI", page_icon="🏁", layout="centered")
    st.title("Pitwall AI")
    st.caption("Formula-1-Wissensassistent mit überprüfbaren Daten und lokalem Wissenskorpus")
    mode = st.sidebar.radio("Modus", ["Hybrid", "Baseline"])
    if mode == "Hybrid":
        st.sidebar.info(
            "Hybrid kann passende Jolpica-Daten und den lokalen Wissenskorpus einbeziehen. "
            "So lassen sich Fakten mit Quellen prüfen."
        )
    else:
        st.sidebar.warning(
            "Baseline antwortet ohne API-Abfragen und Wissenskorpus. Fakten werden nicht "
            "extern überprüft."
        )
    if st.sidebar.button("Chatverlauf löschen"):
        st.session_state.messages = []
    store = VectorStore(settings.chroma_path)
    st.sidebar.write(f"Wissenskorpus: {'verfügbar' if store.available else 'nicht initialisiert'}")
    st.sidebar.write(f"Datenstand: {settings.f1_end_season}")
    if not settings.openai_api_key or not settings.openai_model:
        st.sidebar.info("Für Antworten bitte OPENAI_API_KEY und OPENAI_MODEL in .env setzen.")
    # Streamlit reruns this script after interactions, so the chat history must persist in session state.
    if "messages" not in st.session_state:
        st.session_state.messages = []
    selected_example = st.session_state.pop("selected_example", None)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                _render_charts(message.get("charts", []))
    _render_examples(mode)
    typed_question = st.chat_input("Deine Frage zur Formel 1")
    if question := selected_example or typed_question:
        _ask(question, mode, settings, store)
    st.divider()
    st.caption(
        "Inoffizieller Hochschulprototyp. Daten: Jolpica F1 API. Keine offiziellen "
        "F1-Logos oder geschützten Bildmaterialien."
    )


@st.fragment(run_every="8s")
def _render_examples(mode: str) -> None:
    """Show a rotating selection of example questions without rerunning the chat."""
    st.markdown("**Beispielfragen**")
    if mode == "Hybrid":
        examples = random.sample(EXAMPLE_QUESTIONS, k=2) + [
            random.choice(CHART_EXAMPLE_QUESTIONS)
        ]
        random.shuffle(examples)
    else:
        examples = random.sample(EXAMPLE_QUESTIONS, k=3)

    for index, example in enumerate(examples):
        st.button(
            example,
            key=f"example_{index}",
            on_click=_select_example,
            args=(example,),
        )


def _select_example(question: str) -> None:
    """Store the clicked question and rerun the full app to answer it."""
    st.session_state.selected_example = question
    st.rerun(scope="app")


def _ask(question: str, mode: str, settings: Settings, store: VectorStore) -> None:
    """Process and display one question."""
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Pitwall AI prüft die Frage ..."):
            # Scope the HTTP client to this question so its connection is closed after the response.
            with JolpicaClient(settings.jolpica_base_url) as client:
                openai_client = (
                    OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
                )
                service = AssistantService(settings, client, store, openai_client)
                answer, used = service.answer(question, mode)
        st.markdown(answer)
        charts = _build_chart_specs(service.last_tool_results)
        _render_charts(charts)
        if used:
            with st.expander("Verwendete Tools"):
                st.write(", ".join(used))
        st.session_state.messages.append({"role": "assistant", "content": answer, "charts": charts})


def _render_charts(charts: list[dict[str, Any]]) -> None:
    """Render chart data created from verified API tool results."""
    for chart in charts:
        st.caption(chart["title"])
        st.bar_chart(chart["data"], width="stretch")


def _build_chart_specs(tool_results: list[tuple[str, Any]]) -> list[dict[str, Any]]:
    """Build simple charts for standings and driver comparison tool results."""
    charts: list[dict[str, Any]] = []
    for tool_name, result in tool_results:
        if not getattr(result, "success", False):
            continue
        data = getattr(result, "data", None)
        if tool_name in {"get_driver_standings", "get_constructor_standings"}:
            chart_data = _standings_data(data, tool_name)
            if chart_data:
                charts.append(
                    {
                        "title": "Punktestand aus den API-Daten",
                        "data": chart_data,
                    }
                )
        elif tool_name == "compare_drivers":
            chart_data = _comparison_data(data)
            if chart_data:
                charts.append({"title": "Fahrervergleich nach Punkten", "data": chart_data})
    return charts


def _standings_data(data: Any, tool_name: str) -> dict[str, float]:
    """Extract names and points from a Jolpica standings response."""
    if not isinstance(data, list):
        return {}
    chart_data: dict[str, float] = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        entity = item.get("Driver" if tool_name == "get_driver_standings" else "Constructor", {})
        if not isinstance(entity, dict):
            continue
        name = entity.get("familyName" if tool_name == "get_driver_standings" else "name")
        points = _to_number(item.get("points"))
        if name and points is not None:
            chart_data[str(name)] = points
    return chart_data


def _comparison_data(data: Any) -> dict[str, float]:
    """Aggregate points for each driver returned by the comparison tool."""
    if not isinstance(data, dict):
        return {}
    chart_data: dict[str, float] = {}
    for driver_key, races in data.items():
        if not isinstance(races, list):
            continue
        total = 0.0
        for race in races:
            if not isinstance(race, dict):
                continue
            result_rows = race.get("Results", [race])
            if isinstance(result_rows, list):
                total += sum(
                    points
                    for row in result_rows
                    if isinstance(row, dict)
                    for points in [_to_number(row.get("points"))]
                    if points is not None
                )
        driver_name = str(driver_key).split(":", 1)[-1]
        chart_data[driver_name] = total
    return chart_data


def _to_number(value: Any) -> float | None:
    """Convert API numeric strings without fabricating missing values."""
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None
