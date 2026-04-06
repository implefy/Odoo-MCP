# Odoo MCP Server

MCP server plugin that connects Claude to your Odoo ERP instance. Supports Sales, Contacts, Invoicing, and Project Management.

## Install

Add the marketplace in Claude Desktop or Claude Code:

```
/plugin marketplace add implefy/Odoo-MCP
/plugin install odoo-erp@implefy-plugins
```

That's it. The server starts automatically. On first use, Claude will ask for your Odoo credentials (URL, database, username, API key) and save them to `~/.odoo-mcp.json`.

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/odoo-erp:quote` | Search or create quotations |
| `/odoo-erp:order-status` | Check sales order status |
| `/odoo-erp:customer` | Look up or create customers |
| `/odoo-erp:invoice` | Search invoices or check outstanding balances |
| `/odoo-erp:task` | Search or create project tasks |

## Available Tools (29 total)

### Setup (2 tools)
`setup_credentials`, `get_credentials_status`

### Sales (6 tools)
`search_quotes`, `get_quote`, `create_quote`, `confirm_quote`, `search_orders`, `cancel_order`

### Contacts (4 tools)
`search_contacts`, `get_contact`, `create_contact`, `update_contact`

### Invoicing (5 tools)
`search_invoices`, `get_invoice`, `create_invoice`, `post_invoice`, `get_outstanding_invoices`

### Projects (5 tools)
`search_projects`, `get_project`, `search_tasks`, `create_task`, `update_task`

### Generic (7 tools)
`search_records`, `get_record`, `count_records`, `get_model_fields`, `search_products`, `create_record`, `update_record`, `delete_record`
