"""Validated assistant tools backed by the Jolpica client and vector store."""

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator

from pitwall_ai.api.jolpica_client import JolpicaClient, JolpicaError
from pitwall_ai.models import SourceMetadata, ToolResult
from pitwall_ai.rag.vector_store import VectorStore


class SeasonInput(BaseModel):
    """Validate a Formula 1 season."""

    season: int = Field(ge=1950, le=2100)


class RaceInput(SeasonInput):
    """Validate a season and optional race round."""

    round_number: int | None = Field(default=None, ge=1, le=100)


class NameInput(BaseModel):
    """Validate a Jolpica identifier or search name."""

    name: str = Field(min_length=1, max_length=80)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Reject URL-like and control input."""
        if any(character in value for character in ("/", "\\", "?", "#")):
            raise ValueError("Names must not contain URL or path characters.")
        return value.strip()


def _result(data: Any, endpoint: str) -> ToolResult:
    return ToolResult(
        success=True,
        data=data,
        source=SourceMetadata(source_type="api", endpoint=endpoint, retrieved_at=datetime.now(timezone.utc)),
    )


def _error(error: Exception, endpoint: str) -> ToolResult:
    return ToolResult(
        success=False,
        error=str(error),
        source=SourceMetadata(source_type="api", endpoint=endpoint, retrieved_at=datetime.now(timezone.utc)),
    )


def get_season_schedule(client: JolpicaClient, season: int) -> ToolResult:
    """Return a validated season schedule."""
    endpoint = f"{client.base_url}/{season}.json"
    try:
        return _result(client.get_season_schedule(str(season)), endpoint)
    except (JolpicaError, ValueError) as error:
        return _error(error, endpoint)


def get_race_results(client: JolpicaClient, season: int, round_number: int | None = None) -> ToolResult:
    """Return results for a season or a specific round."""
    endpoint = f"{client.base_url}/{season}/results.json"
    try:
        return _result(client.get_race_results(str(season), round_number), endpoint)
    except (JolpicaError, ValueError) as error:
        return _error(error, endpoint)


def get_driver_standings(client: JolpicaClient, season: int) -> ToolResult:
    """Return driver standings."""
    try:
        return _result(client.get_driver_standings(str(season)), f"{client.base_url}/{season}/driverstandings.json")
    except (JolpicaError, ValueError) as error:
        return _error(error, f"{client.base_url}/{season}/driverstandings.json")


def get_constructor_standings(client: JolpicaClient, season: int) -> ToolResult:
    """Return constructor standings."""
    try:
        return _result(client.get_constructor_standings(str(season)), f"{client.base_url}/{season}/constructorstandings.json")
    except (JolpicaError, ValueError) as error:
        return _error(error, f"{client.base_url}/{season}/constructorstandings.json")


def get_circuit_information(client: JolpicaClient, name: str) -> ToolResult:
    """Return circuit information."""
    validated = NameInput(name=name)
    endpoint = f"{client.base_url}/circuits/{validated.name}.json"
    try:
        return _result(client.get_circuit_information(validated.name), endpoint)
    except (JolpicaError, ValueError) as error:
        return _error(error, endpoint)


def get_driver_information(client: JolpicaClient, name: str) -> ToolResult:
    """Return driver information."""
    validated = NameInput(name=name)
    endpoint = f"{client.base_url}/drivers/{validated.name}.json"
    try:
        return _result(client.get_driver_information(validated.name), endpoint)
    except (JolpicaError, ValueError) as error:
        return _error(error, endpoint)


def get_constructor_information(client: JolpicaClient, name: str) -> ToolResult:
    """Return constructor information."""
    validated = NameInput(name=name)
    endpoint = f"{client.base_url}/constructors/{validated.name}.json"
    try:
        return _result(client.get_constructor_information(validated.name), endpoint)
    except (JolpicaError, ValueError) as error:
        return _error(error, endpoint)


def get_driver_season_results(client: JolpicaClient, season: int, driver: str) -> ToolResult:
    """Return one driver's results for a season."""
    validated = NameInput(name=driver)
    endpoint = f"{client.base_url}/{season}/drivers/{validated.name}/results.json"
    try:
        return _result(client.get_driver_season_results(str(season), validated.name), endpoint)
    except (JolpicaError, ValueError) as error:
        return _error(error, endpoint)


def compare_drivers(client: JolpicaClient, start_season: int, end_season: int, drivers: list[str]) -> ToolResult:
    """Return season results for multiple drivers across a bounded range."""
    # Each season-driver pair makes a separate API request, so bound the total fan-out.
    if start_season > end_season or end_season - start_season > 10 or not 2 <= len(drivers) <= 4:
        return _error(ValueError("Use a range of at most ten seasons and two to four drivers."), "")
    data: dict[str, Any] = {}
    for season in range(start_season, end_season + 1):
        for driver in drivers:
            data[f"{season}:{driver}"] = get_driver_season_results(client, season, driver).data
    return _result(data, f"{client.base_url}/{start_season}-{end_season}/drivers/results")


def search_knowledge_base(store: VectorStore, query: str) -> ToolResult:
    """Search bounded local context while treating documents as untrusted data."""
    if not query.strip():
        return _error(ValueError("The search query must not be empty."), "local://knowledge-base")
    return ToolResult(
        success=True,
        data=[item.model_dump() for item in store.search(query[:500], limit=5)],
        source=SourceMetadata(source_type="knowledge_base", endpoint="local://knowledge-base", retrieved_at=datetime.now(timezone.utc)),
    )
