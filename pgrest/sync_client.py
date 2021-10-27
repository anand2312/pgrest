from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from httpx import Client as _Client
from httpx import Response

from pgrest.base_client import BaseClient
from pgrest.constants import DEFAULT_POSTGREST_CLIENT_HEADERS


class Client(BaseClient):
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

    def __enter__(self) -> Client:
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

    def rpc(self, func: str, params: dict) -> Response:
        """Perform a stored procedure call."""
        path = self._get_rpc_path(func)
        r = self.session.post(path, json=params)
        return r
