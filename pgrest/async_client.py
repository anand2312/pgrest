from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from httpx import AsyncClient as _AsyncClient
from httpx import Response

from pgrest.base_client import BaseClient
from pgrest.constants import DEFAULT_POSTGREST_CLIENT_HEADERS


class AsyncClient(BaseClient):
    """Asyncio compatible PostgREST client."""

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
        self.session: _AsyncClient = _AsyncClient(base_url=base_url, headers=headers)

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self.session.aclose()

    async def rpc(self, func: str, params: dict) -> Response:
        """Perform a stored procedure call."""
        path = self._get_rpc_path(func)
        r = await self.session.post(path, json=params)
        return r
