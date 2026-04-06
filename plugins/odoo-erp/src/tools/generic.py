"""Generic/utility tools — search any model, inspect fields, etc."""

from __future__ import annotations
from typing import Any

from mcp.server.fastmcp import FastMCP

from src.odoo_client import OdooClient


def register_generic_tools(mcp: FastMCP, get_client: callable) -> None:
    """Register generic utility tools on the MCP server."""

    @mcp.tool()
    def search_records(
        model: str,
        domain: list | None = None,
        fields: list[str] | None = None,
        limit: int = 20,
        offset: int = 0,
        order: str | None = None,
    ) -> list[dict]:
        """Search any Odoo model with a domain filter. Power-user tool.

        Args:
            model: Odoo model name (e.g. 'res.partner', 'product.product').
            domain: Odoo domain filter as a list of tuples,
                    e.g. [["state","=","draft"],["name","ilike","test"]].
            fields: List of field names to return. If empty, returns all.
            limit: Max records to return.
            offset: Pagination offset.
            order: Sort order (e.g. 'name asc', 'create_date desc').
        """
        client = get_client()
        return client.search_read(
            model, domain, fields, limit=limit, offset=offset, order=order
        )

    @mcp.tool()
    def get_record(model: str, record_id: int, fields: list[str] | None = None) -> dict:
        """Read a single record from any Odoo model by ID.

        Args:
            model: Odoo model name (e.g. 'sale.order').
            record_id: The record ID.
            fields: List of field names to return. If empty, returns all.
        """
        client = get_client()
        records = client.read(model, [record_id], fields)
        if not records:
            return {"error": f"Record {record_id} not found in {model}"}
        return records[0]

    @mcp.tool()
    def count_records(model: str, domain: list | None = None) -> dict:
        """Count records matching a domain filter in any Odoo model.

        Args:
            model: Odoo model name.
            domain: Odoo domain filter.
        """
        client = get_client()
        count = client.search_count(model, domain)
        return {"model": model, "count": count}

    @mcp.tool()
    def get_model_fields(
        model: str,
        field_names: list[str] | None = None,
    ) -> dict:
        """Get field definitions for an Odoo model. Useful for understanding
        what fields are available before searching or creating records.

        Args:
            model: Odoo model name (e.g. 'sale.order').
            field_names: Specific fields to describe. If empty, returns all fields.
        """
        client = get_client()
        all_fields = client.fields_get(
            model, attributes=["string", "type", "required", "readonly", "selection"]
        )
        if field_names:
            all_fields = {k: v for k, v in all_fields.items() if k in field_names}
        return all_fields

    @mcp.tool()
    def search_products(
        name: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Search for products (useful when creating quotes or invoices).

        Args:
            name: Filter by product name (partial match).
            limit: Max records to return.
        """
        client = get_client()
        domain: list[Any] = [("sale_ok", "=", True)]
        if name:
            domain.append(("name", "ilike", name))
        return client.search_read(
            "product.product", domain,
            ["id", "name", "list_price", "default_code", "type", "categ_id",
             "uom_id", "qty_available"],
            limit=limit, order="name asc",
        )

    @mcp.tool()
    def create_record(model: str, values: dict) -> dict:
        """Create a record in any Odoo model. Power-user tool.

        Args:
            model: Odoo model name (e.g. 'res.partner').
            values: Dict of field name to value for the new record.
        """
        client = get_client()
        new_id = client.create(model, values)
        return client.read(model, [new_id])[0]

    @mcp.tool()
    def update_record(model: str, record_id: int, values: dict) -> dict:
        """Update a record in any Odoo model. Power-user tool.

        Args:
            model: Odoo model name.
            record_id: The record ID to update.
            values: Dict of field name to new value.
        """
        client = get_client()
        client.write(model, [record_id], values)
        return client.read(model, [record_id])[0]

    @mcp.tool()
    def delete_record(model: str, record_id: int) -> dict:
        """Delete a record from any Odoo model. Use with caution.

        Args:
            model: Odoo model name.
            record_id: The record ID to delete.
        """
        client = get_client()
        client.unlink(model, [record_id])
        return {"status": "deleted", "model": model, "id": record_id}
