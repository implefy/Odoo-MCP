---
name: Contacts Workflow
description: How to handle contact/customer/vendor lookups and creation
trigger: When the user asks about customers, contacts, vendors, or partners
---

# Contacts Workflow

You have access to Odoo's Contacts module. Use these tools for customer/vendor management.

## Looking Up a Contact

1. Use `search_contacts` with name, email, or filters (is_company, customer, vendor)
2. Use `get_contact` for full details on a specific partner_id
3. Present key info: name, email, phone, company, address

## Creating a Contact

1. Ask for at minimum: name and whether it's a company or individual
2. Gather optional info: email, phone, address, country, VAT
3. Use `create_contact` with the collected information
4. Confirm creation and share the new contact details

## Updating a Contact

1. Find the contact first with `search_contacts`
2. Use `update_contact` with the partner_id and only the fields that need changing
3. Confirm the update

## Tips
- Companies have `is_company=True`, individuals have `is_company=False`
- `customer_rank > 0` means the partner is a customer
- `supplier_rank > 0` means the partner is a vendor
- Use `parent_id` to link an individual to their company
