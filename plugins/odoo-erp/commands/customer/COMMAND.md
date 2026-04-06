---
name: customer
description: Look up or create a customer in Odoo
usage: /customer [name or email]
---

# /customer Command

When the user runs `/customer`:

- If they provide a name or email, search for matching contacts using `search_contacts`.
- Present results in a clean format: name, email, phone, company, city.
- If no results found, offer to create a new contact.
- If no argument, ask what customer they want to look up.
