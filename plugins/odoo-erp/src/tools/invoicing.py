"""Invoicing module tools — invoices, credit notes, payments."""

from __future__ import annotations
from typing import Any

from mcp.server.fastmcp import FastMCP

from src.odoo_client import OdooClient

INVOICE_FIELDS = [
    "id", "name", "move_type", "partner_id", "invoice_date",
    "invoice_date_due", "amount_total", "amount_residual",
    "amount_untaxed", "amount_tax", "state", "payment_state",
    "ref", "narration", "currency_id", "journal_id",
]

INVOICE_LINE_FIELDS = [
    "id", "product_id", "name", "quantity", "price_unit",
    "price_subtotal", "tax_ids", "discount", "account_id",
]


def register_invoicing_tools(mcp: FastMCP, get_client: callable) -> None:
    """Register all invoicing-related tools on the MCP server."""

    @mcp.tool()
    def search_invoices(
        customer_name: str | None = None,
        state: str | None = None,
        move_type: str = "out_invoice",
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:
        """Search for invoices or credit notes.

        Args:
            customer_name: Filter by customer name (partial match).
            state: Filter by state: 'draft', 'posted', 'cancel'.
            move_type: Type of move: 'out_invoice' (customer invoice),
                       'out_refund' (credit note), 'in_invoice' (vendor bill),
                       'in_refund' (vendor credit note). Default: 'out_invoice'.
            limit: Max records to return.
            offset: Pagination offset.
        """
        client: OdooClient = get_client()
        domain: list[Any] = [("move_type", "=", move_type)]
        if customer_name:
            domain.append(("partner_id.name", "ilike", customer_name))
        if state:
            domain.append(("state", "=", state))
        return client.search_read(
            "account.move", domain, INVOICE_FIELDS, limit=limit, offset=offset,
            order="invoice_date desc",
        )

    @mcp.tool()
    def get_invoice(invoice_id: int, include_lines: bool = True) -> dict:
        """Get a specific invoice by ID, optionally with line items.

        Args:
            invoice_id: The account.move record ID.
            include_lines: Whether to include invoice line details.
        """
        client = get_client()
        records = client.read("account.move", [invoice_id], INVOICE_FIELDS)
        if not records:
            return {"error": f"Invoice {invoice_id} not found"}
        result = records[0]
        if include_lines:
            full = client.execute(
                "account.move", "read", [invoice_id],
                fields=["invoice_line_ids"],
            )
            line_ids = full[0].get("invoice_line_ids", [])
            if line_ids:
                result["lines"] = client.read(
                    "account.move.line", line_ids, INVOICE_LINE_FIELDS
                )
        return result

    @mcp.tool()
    def create_invoice(
        partner_id: int,
        lines: list[dict],
        move_type: str = "out_invoice",
        invoice_date: str | None = None,
        ref: str | None = None,
    ) -> dict:
        """Create a new invoice (draft).

        Args:
            partner_id: Customer/vendor (res.partner) ID.
            lines: List of line items, each with keys: product_id (int),
                   quantity (float), price_unit (float), name (str, optional),
                   discount (float, optional).
            move_type: 'out_invoice' (customer), 'in_invoice' (vendor).
            invoice_date: Invoice date as 'YYYY-MM-DD'. Defaults to today.
            ref: Payment reference / vendor bill number.
        """
        client = get_client()
        invoice_lines = []
        for line in lines:
            vals: dict[str, Any] = {
                "product_id": line["product_id"],
                "quantity": line.get("quantity", 1),
            }
            if "price_unit" in line:
                vals["price_unit"] = line["price_unit"]
            if "name" in line:
                vals["name"] = line["name"]
            if "discount" in line:
                vals["discount"] = line["discount"]
            invoice_lines.append((0, 0, vals))

        values: dict[str, Any] = {
            "move_type": move_type,
            "partner_id": partner_id,
            "invoice_line_ids": invoice_lines,
        }
        if invoice_date:
            values["invoice_date"] = invoice_date
        if ref:
            values["ref"] = ref

        new_id = client.create("account.move", values)
        return client.read("account.move", [new_id], INVOICE_FIELDS)[0]

    @mcp.tool()
    def post_invoice(invoice_id: int) -> dict:
        """Post/confirm a draft invoice, making it official.

        Args:
            invoice_id: The account.move record ID to post.
        """
        client = get_client()
        client.call_method("account.move", "action_post", [invoice_id])
        return client.read("account.move", [invoice_id], INVOICE_FIELDS)[0]

    @mcp.tool()
    def get_outstanding_invoices(
        customer_name: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Get invoices that have an outstanding balance (not fully paid).

        Args:
            customer_name: Optional filter by customer name.
            limit: Max records to return.
        """
        client = get_client()
        domain: list[Any] = [
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("amount_residual", ">", 0),
        ]
        if customer_name:
            domain.append(("partner_id.name", "ilike", customer_name))
        return client.search_read(
            "account.move", domain, INVOICE_FIELDS, limit=limit,
            order="invoice_date_due asc",
        )
