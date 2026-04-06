---
name: quote
description: Create or search for quotations in Odoo
usage: /quote [search term or "create"]
---

# /quote Command

When the user runs `/quote`:

- If they provide a search term (e.g., `/quote Acme Corp`), search for quotations matching that customer name using `search_quotes`.
- If they say "create" (e.g., `/quote create`), walk them through creating a new quotation:
  1. Ask for the customer name, then look them up with `search_contacts`
  2. Ask for products/services, look them up with `search_products`
  3. Ask for quantities and any discounts
  4. Create the quote with `create_quote`
  5. Present the created quote details
- If no argument, show recent draft quotations using `search_quotes` with default params.
