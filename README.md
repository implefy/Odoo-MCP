# Odoo MCP Server

MCP server that connects Claude to your Odoo ERP instance. Supports Sales, Contacts, Invoicing, and Project Management.

## Setup for Cowork (Claude Desktop)

Cowork runs in a sandbox that can't reach the internet, so the MCP server runs on your machine and Cowork connects to it over HTTP.

### Step 1: Configure your Odoo credentials

Copy `.env.example` to `.env` inside `plugins/odoo-erp/` and fill in your values:

```env
ODOO_URL=https://implefy-implefy-ab.odoo.com
ODOO_DB=implefy-implefy-ab
ODOO_USERNAME=your-email@example.com
ODOO_API_KEY=your-api-key-here
```

### Step 2: Start the MCP server

```bash
cd plugins/odoo-erp
start.bat          # Windows
# or
./start.sh         # Mac/Linux
```

This starts the server at `http://localhost:8000/mcp`. Keep this terminal open.

### Step 3: Add the plugin in Cowork

```
/plugin marketplace add implefy/Odoo-MCP
/plugin install odoo-erp@implefy-plugins
```

The plugin connects to your local MCP server automatically.

### Generate an Odoo API Key

1. Log in to your Odoo instance
2. Go to **Settings > Users & Companies > Users**
3. Click your user, then the **Account Security** tab
4. Under **API Keys**, click **New API Key**
5. Name it "Claude MCP" and copy the key

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
