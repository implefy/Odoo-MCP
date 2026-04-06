---
name: Invoicing Workflow
description: How to handle invoice-related requests — searching, creating, and posting invoices
trigger: When the user asks about invoices, billing, payments, credit notes, or outstanding balances
---

# Invoicing Workflow

You have access to Odoo's Invoicing module through the MCP connector.

## Searching Invoices

1. Use `search_invoices` with optional customer name, state, and move_type filters
2. For overdue/unpaid invoices, use `get_outstanding_invoices`
3. Present: invoice number, customer, date, total, amount due, payment status

## Creating an Invoice

1. Find the customer with `search_contacts`
2. Find products with `search_products`
3. Use `create_invoice` with partner_id, line items, and optional date/reference
4. The invoice is created in **draft** state
5. Share the invoice details

## Posting an Invoice

1. Use `post_invoice` to confirm a draft invoice
2. This makes the invoice official and creates journal entries
3. Once posted, the invoice cannot be easily modified

## Invoice Types (move_type)
- **out_invoice**: Customer invoice (you bill a customer)
- **out_refund**: Customer credit note
- **in_invoice**: Vendor bill (vendor bills you)
- **in_refund**: Vendor credit note

## Payment States
- **not_paid**: Nothing paid yet
- **partial**: Partially paid
- **paid**: Fully paid
- **reversed**: Payment reversed
