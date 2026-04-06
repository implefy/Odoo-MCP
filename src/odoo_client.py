"""Odoo XML-RPC client wrapper."""

import xmlrpc.client
from typing import Any


class OdooClient:
    """Wrapper around Odoo's XML-RPC External API."""

    def __init__(self, url: str, db: str, username: str, api_key: str):
        self.url = url.rstrip("/")
        self.db = db
        self.username = username
        self.api_key = api_key
        self._uid: int | None = None

        self._common = xmlrpc.client.ServerProxy(
            f"{self.url}/xmlrpc/2/common", allow_none=True
        )
        self._object = xmlrpc.client.ServerProxy(
            f"{self.url}/xmlrpc/2/object", allow_none=True
        )

    @property
    def uid(self) -> int:
        if self._uid is None:
            self._uid = self._common.authenticate(
                self.db, self.username, self.api_key, {}
            )
            if not self._uid:
                raise ConnectionError(
                    f"Authentication failed for {self.username} on {self.db}"
                )
        return self._uid

    def execute(
        self, model: str, method: str, *args: Any, **kwargs: Any
    ) -> Any:
        return self._object.execute_kw(
            self.db, self.uid, self.api_key, model, method, list(args), kwargs
        )

    def search_read(
        self,
        model: str,
        domain: list | None = None,
        fields: list[str] | None = None,
        limit: int = 80,
        offset: int = 0,
        order: str | None = None,
    ) -> list[dict]:
        kwargs: dict[str, Any] = {"limit": limit, "offset": offset}
        if fields:
            kwargs["fields"] = fields
        if order:
            kwargs["order"] = order
        return self.execute(model, "search_read", domain or [], **kwargs)

    def read(
        self, model: str, ids: list[int], fields: list[str] | None = None
    ) -> list[dict]:
        kwargs: dict[str, Any] = {}
        if fields:
            kwargs["fields"] = fields
        return self.execute(model, "read", ids, **kwargs)

    def create(self, model: str, values: dict) -> int:
        return self.execute(model, "create", [values])

    def write(self, model: str, ids: list[int], values: dict) -> bool:
        return self.execute(model, "write", ids, values)

    def unlink(self, model: str, ids: list[int]) -> bool:
        return self.execute(model, "unlink", ids)

    def search_count(self, model: str, domain: list | None = None) -> int:
        return self.execute(model, "search_count", domain or [])

    def fields_get(
        self, model: str, attributes: list[str] | None = None
    ) -> dict:
        kwargs: dict[str, Any] = {}
        if attributes:
            kwargs["attributes"] = attributes
        return self.execute(model, "fields_get", **kwargs)

    def call_method(
        self, model: str, method: str, ids: list[int], *args: Any
    ) -> Any:
        return self.execute(model, method, ids, *args)

    def check_connection(self) -> dict:
        version = self._common.version()
        _ = self.uid  # trigger auth
        return {
            "status": "connected",
            "server_version": version.get("server_version", "unknown"),
            "uid": self.uid,
            "database": self.db,
        }
