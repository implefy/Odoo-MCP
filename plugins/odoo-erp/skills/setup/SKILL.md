---
description: Automatically check Odoo connection status and guide the user through setup if needed
trigger: Always run this check before using any Odoo tool for the first time in a conversation
---

# Odoo Setup Check

Before using any Odoo tool, call `get_credentials_status` first.

- If `configured: false`, ask the user for their Odoo URL, database name, login email, and API key, then call `setup_credentials` with those values.
- If `configured: true` and `connected: true`, proceed normally.
- If `configured: true` and `connected: false`, show the error and offer to reconfigure with `setup_credentials`.

When asking for credentials, explain:
- The **URL** is their Odoo instance address (e.g. `https://mycompany.odoo.com`)
- The **database name** is usually the subdomain (e.g. `mycompany-production`)
- The **API key** can be generated at Settings > Users > (their user) > Account Security > API Keys
