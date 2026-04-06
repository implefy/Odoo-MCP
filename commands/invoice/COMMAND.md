---
name: invoice
description: Search invoices or check outstanding balances
usage: /invoice [customer name or "outstanding"]
---

# /invoice Command

When the user runs `/invoice`:

- If they say "outstanding" (e.g., `/invoice outstanding`), use `get_outstanding_invoices` to show unpaid invoices sorted by due date.
- If they provide a customer name, use `search_invoices` with the customer_name filter.
- Present: invoice number, customer, date, total, amount due, payment status.
- If no argument, show the 10 most recent posted invoices.
