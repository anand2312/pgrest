from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from httpx import Client as _Client

from pgrest.base_client import BaseClient
from pgrest.constants import DEFAULT_POSTGREST_CLIENT_HEADERS


class SyncClient(BaseClient):
    """Synchronous PostgREST client."""

    def __init__(
        self,
        base_url: str,
        *,
        schema: str = "public",
        headers: dict[str, str] = DEFAULT_POSTGREST_CLIENT_HEADERS,
    ) -> None:
        headers = {
            **headers,
            "Accept-Profile": schema,
            "Content-Profile": schema,
        }
        self.session: _Client = _Client(base_url=base_url, headers=headers)
        self._models = {}
        self._enums = {}

    def __enter__(self) -> SyncClient:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.session.close()

    def close(self) -> None:
        """Close the underlying HTTP transport and proxies."""
        self.session.close()

    def fetch_database_types(self) -> None:
        """
        Fetch the database models and enumerations from the openapi.json file hosted by PostgREST, and cache them.

        !!! warn
            This method only needs to be called if you want the responses to be parsed into Pydantic objects.
        """
