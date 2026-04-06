"""Odoo MCP Server — main entry point."""

import os

from mcp.server.fastmcp import FastMCP

from src.odoo_client import OdooClient
from src.tools.sales import register_sales_tools
from src.tools.contacts import register_contacts_tools
from src.tools.invoicing import register_invoicing_tools
from src.tools.projects import register_projects_tools
from src.tools.generic import register_generic_tools

mcp = FastMCP(
    "Odoo MCP Server",
    description=(
        "MCP server for Odoo ERP. Provides tools for Sales (quotes, orders), "
        "Contacts, Invoicing, and Project Management."
    ),
)

_client: OdooClient | None = None


def get_client() -> OdooClient:
    """Lazy-initialize and return the Odoo client singleton."""
    global _client
    if _client is None:
        url = os.environ.get("ODOO_URL", "")
        db = os.environ.get("ODOO_DB", "")
        username = os.environ.get("ODOO_USERNAME", "")
        api_key = os.environ.get("ODOO_API_KEY", "")

        if not all([url, db, username, api_key]):
            missing = [
                k for k in ["ODOO_URL", "ODOO_DB", "ODOO_USERNAME", "ODOO_API_KEY"]
                if not os.environ.get(k)
            ]
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Set them in a .env file or as environment variables."
            )

        _client = OdooClient(url, db, username, api_key)
    return _client


# Register all tool modules
register_sales_tools(mcp, get_client)
register_contacts_tools(mcp, get_client)
register_invoicing_tools(mcp, get_client)
register_projects_tools(mcp, get_client)
register_generic_tools(mcp, get_client)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
