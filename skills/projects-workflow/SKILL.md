---
name: Projects Workflow
description: How to handle project and task management requests
trigger: When the user asks about projects, tasks, timesheets, or work assignments
---

# Projects Workflow

You have access to Odoo's Project module through the MCP connector.

## Searching Projects & Tasks

1. Use `search_projects` to find projects by name
2. Use `search_tasks` to find tasks, with filters for project, assignee, stage, or priority
3. Present: task name, project, assignee, deadline, stage, hours

## Creating a Task

1. Find the project first with `search_projects`
2. Use `create_task` with the project_id, name, and optional details
3. Optionally assign users with user_ids, set deadline, planned hours, priority
4. For sub-tasks, set the parent_id

## Updating a Task

1. Find the task with `search_tasks`
2. Use `update_task` with the task_id and fields to change
3. Common updates: stage changes, priority, deadline, description

## Priority Levels
- **0**: Normal
- **1**: Important / Urgent
