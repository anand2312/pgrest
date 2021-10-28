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
        Bearer token is preferred if both ones are provided.

        Args:
            token: The bearer token to authenticate with.
            username: Username
            password: Password
        Returns:
            The modified Client instance.
        Raises:
            ValueError: if neither authentication scheme is provided.
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
        """
        Switch to another database schema.

        Args:
            schema: The name of the new schema to switch to.
        Returns:
            The modified Client instance.
        """
        self.session.headers.update({"Accept-Profile": schema, "Content-Profile": schema})
        return self

    def from_(self, table: str) -> RequestBuilder:
        """
        Perform a table operation.

        Args:
            table: The name of the table to query from.
        Returns:
            RequestBuilder
        """
        return RequestBuilder(self.session, f"/{table}")

    def rpc(self, func: str, params: dict) -> FilterRequestBuilder:
        """
        Perform a stored procedure call.

        Args:
            func: The name of the PostgreSQL stored procedure (function) to run.
            params: Named parameters to pass to the function.
        Returns:
            FilterRequestBuilder: Apply filters to the result of the function, if the function returns a table.
        """
        path = self._get_rpc_path(func)
        return FilterRequestBuilder(self.session, path, "POST", params)
