---
name: order-status
description: Check the status of sales orders
usage: /order-status [customer name or order number]
---

# /order-status Command

When the user runs `/order-status`:

- If they provide a customer name, search for their orders using `search_orders` with the customer_name filter.
- If they provide an order number (e.g., S00042), use `search_records` with model "sale.order" and domain `[["name","=","S00042"]]`.
- Show: order number, customer, date, total amount, and current state.
- If no argument, show the 10 most recent confirmed orders.
