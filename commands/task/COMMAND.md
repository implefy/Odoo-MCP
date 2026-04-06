---
name: task
description: Search or create project tasks in Odoo
usage: /task [search term or "create"]
---

# /task Command

When the user runs `/task`:

- If they provide a search term, use `search_tasks` to find matching tasks.
- If they say "create" (e.g., `/task create`), walk them through:
  1. Ask for the project (look up with `search_projects`)
  2. Ask for task name and description
  3. Ask for assignee, deadline, priority (optional)
  4. Create with `create_task`
- If no argument, show recent tasks across all projects.
