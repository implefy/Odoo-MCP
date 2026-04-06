---
name: Sales Workflow
description: How to handle sales-related requests — creating quotes, checking order status, confirming orders
trigger: When the user asks about quotes, sales orders, pricing, or deals
---

# Sales Workflow

You have access to Odoo's Sales module through the MCP connector. Use these tools for sales-related requests.

## Creating a Quote

1. First, find the customer using `search_contacts` by name or email
2. Find the products using `search_products` by name
3. Create the quote using `create_quote` with the partner_id and product lines
4. Share the quote details with the user (quote number, total, line items)

## Checking Order Status

1. Use `search_orders` to find confirmed sales orders, or `search_quotes` for drafts
2. Use `get_quote` with `include_lines=true` to see full details
3. Summarize: order number, customer, total, status, and line items

## Confirming a Quote

1. Use `confirm_quote` with the order_id
2. This converts the draft quotation into a confirmed sales order
3. Confirm success and share the updated status

## Key States
- **draft**: Quotation (not yet sent)
- **sent**: Quotation sent to customer
- **sale**: Confirmed sales order
- **done**: Locked/completed
- **cancel**: Cancelled
