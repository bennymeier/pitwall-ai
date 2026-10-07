"""Typed client for the compatible Jolpica Ergast API."""

from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


class JolpicaError(RuntimeError):
    """Represent a safe API client error."""


class JolpicaClient:
    """Fetch Formula 1 data through allow-listed API paths."""

    def __init__(self, base_url: str, timeout: float = 15.0, transport: httpx.BaseTransport | None = None) -> None:
        """Initialize the client with a base URL and HTTP timeout."""
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=timeout, transport=transport)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "JolpicaClient":
        """Enter the client context manager."""
        return self

    def __exit__(self, *_: object) -> None:
        """Close the client when leaving a context manager."""
        self.close()

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        wait=wait_exponential(multiplier=0.2, min=0.2, max=2),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def _get(self, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        response = self._client.get(f"{self.base_url}/{path.lstrip('/')}", params=params)
        if response.status_code == 404:
            raise JolpicaError("The requested Formula 1 resource was not found.")
        if response.status_code == 429:
            raise JolpicaError("The Formula 1 API rate limit was reached.")
        if response.status_code >= 500:
            raise JolpicaError("The Formula 1 API is temporarily unavailable.")
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        return payload

    def _get_paged(self, path: str) -> Iterator[dict[str, Any]]:
        offset = 0
        # Jolpica limits each page; use the returned count to request the next slice.
        while True:
            payload = self._get(path, {"limit": "100", "offset": str(offset)})
            mr_data = payload.get("MRData", {})
            yield mr_data
            total = int(mr_data.get("total", 0))
            returned = len(mr_data.get("RaceTable", {}).get("Races", []))
            if returned == 0 or offset + returned >= total:
                return
            offset += returned

    def query(self, path: str) -> dict[str, Any]:
        """Fetch one allow-listed endpoint and return its MRData payload."""
        if not path or path.startswith(("http:", "https:", "//")):
            raise ValueError("Only relative Formula 1 API paths are allowed.")
        parts = path.strip("/").split("/")
        # Keep requests on the configured API host and restrict them to known resource families.
        allowed_roots = {"current", "seasons", "drivers", "constructors", "circuits"}
        is_season_resource = parts and (parts[0].isdigit() or parts[0] == "current")
        is_known_resource = any(part in allowed_roots for part in parts) or is_season_resource
        if not is_known_resource:
            raise ValueError("The requested API resource is not allow-listed.")
        return self._get(path).get("MRData", {})

    def get_season_schedule(self, season: str) -> list[dict[str, Any]]:
        """Return races scheduled for a season."""
        return self._races(f"{season}.json")

    def get_race_results(self, season: str, round_number: int | None = None) -> list[dict[str, Any]]:
        """Return race results for a season or one round."""
        suffix = f"/{round_number}" if round_number is not None else ""
        return self._races(f"{season}{suffix}/results.json")

    def get_driver_standings(self, season: str) -> list[dict[str, Any]]:
        """Return driver standings for a season."""
        return self._standings(f"{season}/driverstandings.json", "DriverStandings")

    def get_constructor_standings(self, season: str) -> list[dict[str, Any]]:
        """Return constructor standings for a season."""
        return self._standings(f"{season}/constructorstandings.json", "ConstructorStandings")

    def get_circuit_information(self, circuit: str) -> list[dict[str, Any]]:
        """Return circuit records matching an identifier."""
        return self._races(f"circuits/{circuit}.json")

    def get_driver_information(self, driver: str) -> list[dict[str, Any]]:
        """Return driver records matching an identifier."""
        return self._races(f"drivers/{driver}.json")

    def get_constructor_information(self, constructor: str) -> list[dict[str, Any]]:
        """Return constructor records matching an identifier."""
        return self._races(f"constructors/{constructor}.json")

    def get_driver_season_results(self, season: str, driver: str) -> list[dict[str, Any]]:
        """Return all race results for a driver in a season."""
        return self._races(f"{season}/drivers/{driver}/results.json")

    def _races(self, path: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for data in self._get_paged(path):
            records.extend(data.get("RaceTable", {}).get("Races", []))
        return records

    def _standings(self, path: str, key: str) -> list[dict[str, Any]]:
        data = self._get(path).get("MRData", {})
        lists = data.get("StandingsTable", {}).get("StandingsLists", [])
        return lists[0].get(key, []) if lists else []

    @staticmethod
    def retrieved_at() -> datetime:
        """Return a timezone-aware retrieval timestamp."""
        return datetime.now(timezone.utc)
