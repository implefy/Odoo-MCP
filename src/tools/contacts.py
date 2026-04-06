"""Contacts module tools — customers, vendors, partners."""

from __future__ import annotations
from typing import Any

from mcp.server.fastmcp import FastMCP

from src.odoo_client import OdooClient

CONTACT_FIELDS = [
    "id", "name", "email", "phone", "mobile", "street", "street2",
    "city", "state_id", "zip", "country_id", "website", "vat",
    "is_company", "company_type", "parent_id", "customer_rank",
    "supplier_rank", "comment",
]


def register_contacts_tools(mcp: FastMCP, get_client: callable) -> None:
    """Register all contact-related tools on the MCP server."""

    @mcp.tool()
    def search_contacts(
        name: str | None = None,
        email: str | None = None,
        is_company: bool | None = None,
        customer: bool = False,
        vendor: bool = False,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:
        """Search for contacts/partners in Odoo.

        Args:
            name: Filter by name (partial match).
            email: Filter by email (partial match).
            is_company: True for companies only, False for individuals only.
            customer: If True, only return customers (customer_rank > 0).
            vendor: If True, only return vendors (supplier_rank > 0).
            limit: Max records to return.
            offset: Pagination offset.
        """
        client: OdooClient = get_client()
        domain: list[Any] = []
        if name:
            domain.append(("name", "ilike", name))
        if email:
            domain.append(("email", "ilike", email))
        if is_company is not None:
            domain.append(("is_company", "=", is_company))
        if customer:
            domain.append(("customer_rank", ">", 0))
        if vendor:
            domain.append(("supplier_rank", ">", 0))
        return client.search_read(
            "res.partner", domain, CONTACT_FIELDS, limit=limit, offset=offset,
            order="name asc",
        )

    @mcp.tool()
    def get_contact(partner_id: int) -> dict:
        """Get a specific contact/partner by ID.

        Args:
            partner_id: The res.partner record ID.
        """
        client = get_client()
        records = client.read("res.partner", [partner_id], CONTACT_FIELDS)
        if not records:
            return {"error": f"Contact {partner_id} not found"}
        return records[0]

    @mcp.tool()
    def create_contact(
        name: str,
        email: str | None = None,
        phone: str | None = None,
        is_company: bool = False,
        street: str | None = None,
        city: str | None = None,
        zip_code: str | None = None,
        country_code: str | None = None,
        website: str | None = None,
        vat: str | None = None,
        comment: str | None = None,
    ) -> dict:
        """Create a new contact/partner.

        Args:
            name: Contact or company name.
            email: Email address.
            phone: Phone number.
            is_company: True to create a company, False for an individual.
            street: Street address.
            city: City.
            zip_code: Postal/ZIP code.
            country_code: Two-letter country code (e.g. 'US', 'FR').
            website: Website URL.
            vat: Tax ID / VAT number.
            comment: Internal notes.
        """
        client = get_client()
        values: dict[str, Any] = {
            "name": name,
            "is_company": is_company,
            "company_type": "company" if is_company else "person",
        }
        if email:
            values["email"] = email
        if phone:
            values["phone"] = phone
        if street:
            values["street"] = street
        if city:
            values["city"] = city
        if zip_code:
            values["zip"] = zip_code
        if website:
            values["website"] = website
        if vat:
            values["vat"] = vat
        if comment:
            values["comment"] = comment
        if country_code:
            countries = client.search_read(
                "res.country", [("code", "=", country_code.upper())],
                ["id"], limit=1,
            )
            if countries:
                values["country_id"] = countries[0]["id"]

        new_id = client.create("res.partner", values)
        return client.read("res.partner", [new_id], CONTACT_FIELDS)[0]

    @mcp.tool()
    def update_contact(partner_id: int, values: dict) -> dict:
        """Update an existing contact/partner.

        Args:
            partner_id: The res.partner record ID.
            values: Dict of field names to new values. Common fields:
                    name, email, phone, mobile, street, city, zip, website, comment.
        """
        client = get_client()
        client.write("res.partner", [partner_id], values)
        return client.read("res.partner", [partner_id], CONTACT_FIELDS)[0]
