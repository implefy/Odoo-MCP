"""Sales module tools — quotes and orders."""

from __future__ import annotations
from typing import Any

from mcp.server.fastmcp import FastMCP

from src.odoo_client import OdooClient

QUOTE_FIELDS = [
    "id", "name", "partner_id", "date_order", "amount_total",
    "amount_untaxed", "amount_tax", "state", "user_id",
    "validity_date", "note", "currency_id",
]

ORDER_LINE_FIELDS = [
    "id", "product_id", "name", "product_uom_qty", "price_unit",
    "price_subtotal", "tax_id", "discount",
]


def register_sales_tools(mcp: FastMCP, get_client: callable) -> None:
    """Register all sales-related tools on the MCP server."""

    @mcp.tool()
    def search_quotes(
        customer_name: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:
        """Search for draft quotations (sale.order in draft/sent state).

        Args:
            customer_name: Optional filter by customer name (partial match).
            limit: Max records to return (default 20).
            offset: Number of records to skip for pagination.
        """
        client: OdooClient = get_client()
        domain: list[Any] = [("state", "in", ["draft", "sent"])]
        if customer_name:
            domain.append(("partner_id.name", "ilike", customer_name))
        return client.search_read(
            "sale.order", domain, QUOTE_FIELDS, limit=limit, offset=offset,
            order="create_date desc",
        )

    @mcp.tool()
    def get_quote(order_id: int, include_lines: bool = True) -> dict:
        """Get a specific quotation/sales order by ID, optionally with line items.

        Args:
            order_id: The sale.order record ID.
            include_lines: Whether to include order line details (default True).
        """
        client = get_client()
        records = client.read("sale.order", [order_id], QUOTE_FIELDS)
        if not records:
            return {"error": f"Quote {order_id} not found"}
        result = records[0]
        if include_lines:
            line_ids = client.execute(
                "sale.order", "read", [order_id], fields=["order_line"]
            )[0].get("order_line", [])
            if line_ids:
                result["lines"] = client.read(
                    "sale.order.line", line_ids, ORDER_LINE_FIELDS
                )
        return result

    @mcp.tool()
    def create_quote(
        partner_id: int,
        lines: list[dict],
        validity_days: int | None = None,
        note: str | None = None,
    ) -> dict:
        """Create a new quotation.

        Args:
            partner_id: Customer (res.partner) ID.
            lines: List of line items, each with keys: product_id (int),
                   quantity (float), price_unit (float, optional),
                   discount (float, optional).
            validity_days: Number of days the quote is valid.
            note: Internal note on the quotation.
        """
        client = get_client()
        order_lines = []
        for line in lines:
            vals = {
                "product_id": line["product_id"],
                "product_uom_qty": line.get("quantity", 1),
            }
            if "price_unit" in line:
                vals["price_unit"] = line["price_unit"]
            if "discount" in line:
                vals["discount"] = line["discount"]
            order_lines.append((0, 0, vals))

        values: dict[str, Any] = {
            "partner_id": partner_id,
            "order_line": order_lines,
        }
        if validity_days is not None:
            values["validity_date"] = False  # Odoo computes from validity_days
        if note:
            values["note"] = note

        new_id = client.create("sale.order", values)
        return client.read("sale.order", [new_id], QUOTE_FIELDS)[0]

    @mcp.tool()
    def confirm_quote(order_id: int) -> dict:
        """Confirm a draft quotation, converting it to a sales order.

        Args:
            order_id: The sale.order record ID to confirm.
        """
        client = get_client()
        client.call_method("sale.order", "action_confirm", [order_id])
        return client.read("sale.order", [order_id], QUOTE_FIELDS)[0]

    @mcp.tool()
    def search_orders(
        customer_name: str | None = None,
        state: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:
        """Search confirmed sales orders.

        Args:
            customer_name: Optional filter by customer name (partial match).
            state: Filter by state: 'sale' (confirmed), 'done' (locked), 'cancel'.
                   Defaults to showing confirmed orders.
            limit: Max records to return.
            offset: Pagination offset.
        """
        client = get_client()
        domain: list[Any] = [("state", "=", state or "sale")]
        if customer_name:
            domain.append(("partner_id.name", "ilike", customer_name))
        return client.search_read(
            "sale.order", domain, QUOTE_FIELDS, limit=limit, offset=offset,
            order="date_order desc",
        )

    @mcp.tool()
    def cancel_order(order_id: int) -> dict:
        """Cancel a sales order or quotation.

        Args:
            order_id: The sale.order record ID to cancel.
        """
        client = get_client()
        client.call_method("sale.order", "action_cancel", [order_id])
        return client.read("sale.order", [order_id], QUOTE_FIELDS)[0]
