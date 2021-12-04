from __future__ import annotations

from enum import Enum
from typing import AnyStr, Optional, TypeVar, Union

from httpx import AsyncClient, BasicAuth, Client
from pydantic import BaseModel

from pgrest.request_builder import FilterRequestBuilder, RequestBuilder

T = TypeVar("T", bound="BaseClient")


class BaseClient:
    def __init__(self) -> None:
        self.session: Union[Client, AsyncClient]
        self._models: dict[str, BaseModel]
        self._enums: dict[str, Enum]

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
            [RequestBuilder][pgrest.request_builder.RequestBuilder]
        """
        return RequestBuilder(self.session, f"/{table}")

    def rpc(self, func: str, params: dict) -> FilterRequestBuilder:
        """
        Perform a stored procedure call.

        Args:
            func: The name of the PostgreSQL stored procedure (function) to run.
            params: Named parameters to pass to the function.
        Returns:
            [FilterRequestBuilder][pgrest.request_builder.FilterRequestBuilder]
        """
        path = self._get_rpc_path(func)
        return FilterRequestBuilder(self.session, path, "POST", params)

    def fetch_database_types(self) -> None:
        """
        Fetch the database models and enumerations from the openapi.json file hosted by PostgREST, and cache them.

        !!! warn
            This method only needs to be called if you want the responses to be parsed into Pydantic objects.
        """
        raise NotImplementedError

    def get_model(self, table: str) -> Optional[BaseModel]:
        """
        Get the [Model](https://pydantic-docs.helpmanual.io/usage/models/) associated with the specified table, from the client's cache.

        Args:
            table: The name of the table to fetch the Model for
        Returns:
            Model: The associated Model.
            None: If the model was not cached.
        """
        return self._models.get(table)

    def get_enum(self, enum: str) -> Optional[Enum]:
        """
        Get the Python [Enum](https://docs.python.org/3/library/enum.html#enum.Enum) associated with an enum defined in SQL.

        Args:
            enum: The fully qualified name of the enum. For example: If an enum is named `colors` under the `public` schema, pass `public.colors`
        Returns:
            Enum: The associated Enum.
            None: If the enum was not cached.
        """
        return self._enums.get(enum)
