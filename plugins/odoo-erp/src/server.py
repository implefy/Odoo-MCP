"""Odoo MCP Server — main entry point.

Credentials are stored in ~/.odoo-mcp.json. On first use, Claude will
call setup_credentials to configure the connection — no manual setup needed.
"""

import json
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from src.odoo_client import OdooClient
from src.tools.sales import register_sales_tools
from src.tools.contacts import register_contacts_tools
from src.tools.invoicing import register_invoicing_tools
from src.tools.projects import register_projects_tools
from src.tools.generic import register_generic_tools

CONFIG_PATH = Path.home() / ".odoo-mcp.json"

mcp = FastMCP(
    "Odoo MCP Server",
    description=(
        "MCP server for Odoo ERP. Provides tools for Sales (quotes, orders), "
        "Contacts, Invoicing, and Project Management. "
        "On first use, call setup_credentials to configure the Odoo connection."
    ),
)

_client: OdooClient | None = None


def _load_config() -> dict:
    """Load credentials from ~/.odoo-mcp.json or environment variables."""
    config = {}
    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text())
    return {
        "url": os.environ.get("ODOO_URL") or config.get("url", ""),
        "db": os.environ.get("ODOO_DB") or config.get("db", ""),
        "username": os.environ.get("ODOO_USERNAME") or config.get("username", ""),
        "api_key": os.environ.get("ODOO_API_KEY") or config.get("api_key", ""),
    }


def get_client() -> OdooClient:
    """Lazy-initialize and return the Odoo client singleton."""
    global _client
    if _client is None:
        cfg = _load_config()
        missing = [k for k, v in cfg.items() if not v]
        if missing:
            raise ValueError(
                f"Odoo is not configured yet. Missing: {', '.join(missing)}. "
                "Please call the setup_credentials tool first."
            )
        _client = OdooClient(cfg["url"], cfg["db"], cfg["username"], cfg["api_key"])
    return _client


def reset_client():
    """Reset the client so it re-reads config on next use."""
    global _client
    _client = None


# --- Setup tool (registered directly, not in a module) ---

@mcp.tool()
def setup_credentials(
    url: str,
    db: str,
    username: str,
    api_key: str,
) -> dict:
    """Configure the Odoo connection. Call this before using any other tool.
    Saves credentials to ~/.odoo-mcp.json so you only need to do this once.

    Args:
        url: Odoo instance URL (e.g. 'https://mycompany.odoo.com').
        db: Odoo database name (e.g. 'mycompany-production').
        username: Your Odoo login email.
        api_key: Your Odoo API key (generate at Settings > Users > API Keys).
    """
    config = {
        "url": url.rstrip("/"),
        "db": db,
        "username": username,
        "api_key": api_key,
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    reset_client()
    try:
        info = get_client().check_connection()
        return {"status": "configured", "config_path": str(CONFIG_PATH), **info}
    except Exception as e:
        return {"status": "saved_but_connection_failed", "error": str(e),
                "config_path": str(CONFIG_PATH)}


@mcp.tool()
def get_credentials_status() -> dict:
    """Check whether Odoo credentials are configured and the connection works."""
    cfg = _load_config()
    missing = [k for k, v in cfg.items() if not v]
    if missing:
        return {
            "configured": False,
            "missing": missing,
            "message": "Call setup_credentials to configure the Odoo connection.",
        }
    try:
        reset_client()
        info = get_client().check_connection()
        return {"configured": True, "connected": True, **info}
    except Exception as e:
        return {"configured": True, "connected": False, "error": str(e)}


# Register all tool modules
register_sales_tools(mcp, get_client)
register_contacts_tools(mcp, get_client)
register_invoicing_tools(mcp, get_client)
register_projects_tools(mcp, get_client)
register_generic_tools(mcp, get_client)


def main():
    args = sys.argv[1:]
    if "--http" in args:
        idx = args.index("--http")
        port = int(args[idx + 1]) if idx + 1 < len(args) else 8000
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
