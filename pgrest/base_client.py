from __future__ import annotations

from typing import AnyStr, Optional, TypeVar, Union

from httpx import AsyncClient, BasicAuth, Client

from pgrest.request_builder import FilterRequestBuilder, RequestBuilder

T = TypeVar("T", bound="BaseClient")


class BaseClient:
    def __init__(self) -> None:
        self.session: Union[Client, AsyncClient]

    @staticmethod
    def _get_rpc_path(func: str) -> str:
        return f"/rpc/{func}"

    def auth(
        self: T,
        token: Optional[str] = None,
        *,
        username: Optional[AnyStr] = None,
        password: AnyStr = "",
    ) -> T:
        """
        Authenticate the client with either bearer token or basic authentication.

        Raise `ValueError` if neither authentication scheme is provided.
        Bearer token is preferred if both ones are provided.
        """
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        elif username:
            self.session.auth = BasicAuth(username, password)
        else:
            raise ValueError(
                "Neither bearer token or basic authentication scheme is provided"
            )
        return self

    def schema(self: T, schema: str) -> T:
        """Switch to another schema."""
        self.session.headers.update({"Accept-Profile": schema, "Content-Profile": schema})
        return self

    def from_(self, table: str) -> RequestBuilder:
        """Perform a table operation."""
        return RequestBuilder(self.session, f"/{table}")

    def rpc(self, func: str, params: dict) -> FilterRequestBuilder:
        """Perform a stored procedure call."""
        path = self._get_rpc_path(func)
        return FilterRequestBuilder(self.session, path, "POST", params)
