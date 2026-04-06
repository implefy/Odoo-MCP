# Odoo MCP Server

MCP server that connects Claude to your Odoo ERP instance. Supports Sales, Contacts, Invoicing, and Project Management.

## Install via Claude Desktop App

1. Click the **+** button next to the prompt box in the Code tab
2. Select **Plugins** > **Add plugin**
3. Point it to this folder (or the GitHub repo once published)
4. Fill in your Odoo credentials in `.mcp.json`:
   - `ODOO_URL` — your Odoo instance URL
   - `ODOO_DB` — database name
   - `ODOO_USERNAME` — your login email
   - `ODOO_API_KEY` — API key (see below)
5. Done — the server auto-installs deps via `uv` and starts when Claude needs it

### Generate an Odoo API Key

1. Log in to your Odoo instance
2. Go to **Settings > Users & Companies > Users**
3. Click your user, then the **Account Security** tab
4. Under **API Keys**, click **New API Key**
5. Name it "Claude MCP" and copy the key

### Alternative: Claude Code CLI

```bash
claude --plugin-dir "C:/Users/imple/Odoo MCP"
```

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/odoo-erp:quote` | Search or create quotations |
| `/odoo-erp:order-status` | Check sales order status |
| `/odoo-erp:customer` | Look up or create customers |
| `/odoo-erp:invoice` | Search invoices or check outstanding balances |
| `/odoo-erp:task` | Search or create project tasks |

## Available Tools (27 total)

### Sales (6 tools)
`search_quotes`, `get_quote`, `create_quote`, `confirm_quote`, `search_orders`, `cancel_order`

### Contacts (4 tools)
`search_contacts`, `get_contact`, `create_contact`, `update_contact`

### Invoicing (5 tools)
`search_invoices`, `get_invoice`, `create_invoice`, `post_invoice`, `get_outstanding_invoices`

### Projects (5 tools)
`search_projects`, `get_project`, `search_tasks`, `create_task`, `update_task`

### Generic (9 tools)
`check_connection`, `search_records`, `get_record`, `count_records`, `get_model_fields`, `search_products`, `create_record`, `update_record`, `delete_record`

## Architecture

```
├── .claude-plugin/
│   └── plugin.json        # Plugin manifest
├── .mcp.json              # MCP server config (env vars go here)
├── skills/                # Workflow guides
│   ├── sales-workflow/
│   ├── contacts-workflow/
│   ├── invoicing-workflow/
│   └── projects-workflow/
├── commands/              # Slash commands
│   ├── quote/
│   ├── order-status/
│   ├── customer/
│   ├── invoice/
│   └── task/
├── src/
│   ├── server.py          # FastMCP server entry point
│   ├── odoo_client.py     # XML-RPC client wrapper
│   └── tools/             # Tool modules (sales, contacts, invoicing, projects, generic)
└── pyproject.toml
```
