"""Projects module tools — projects and tasks."""

from __future__ import annotations
from typing import Any

from mcp.server.fastmcp import FastMCP

from src.odoo_client import OdooClient

PROJECT_FIELDS = [
    "id", "name", "user_id", "partner_id", "date_start", "date",
    "description", "task_count", "color", "active",
]

TASK_FIELDS = [
    "id", "name", "project_id", "user_ids", "partner_id",
    "date_deadline", "priority", "stage_id", "state",
    "description", "planned_hours", "effective_hours",
    "remaining_hours", "tag_ids", "parent_id",
]


def register_projects_tools(mcp: FastMCP, get_client: callable) -> None:
    """Register all project-related tools on the MCP server."""

    @mcp.tool()
    def search_projects(
        name: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:
        """Search for projects.

        Args:
            name: Filter by project name (partial match).
            limit: Max records to return.
            offset: Pagination offset.
        """
        client: OdooClient = get_client()
        domain: list[Any] = []
        if name:
            domain.append(("name", "ilike", name))
        return client.search_read(
            "project.project", domain, PROJECT_FIELDS, limit=limit,
            offset=offset, order="name asc",
        )

    @mcp.tool()
    def get_project(project_id: int) -> dict:
        """Get a specific project by ID.

        Args:
            project_id: The project.project record ID.
        """
        client = get_client()
        records = client.read("project.project", [project_id], PROJECT_FIELDS)
        if not records:
            return {"error": f"Project {project_id} not found"}
        return records[0]

    @mcp.tool()
    def search_tasks(
        project_id: int | None = None,
        assignee_name: str | None = None,
        stage: str | None = None,
        priority: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:
        """Search for project tasks.

        Args:
            project_id: Filter by project ID.
            assignee_name: Filter by assigned user name (partial match).
            stage: Filter by stage name (partial match, e.g. 'In Progress').
            priority: Filter by priority: '0' (normal), '1' (important/urgent).
            limit: Max records to return.
            offset: Pagination offset.
        """
        client = get_client()
        domain: list[Any] = []
        if project_id:
            domain.append(("project_id", "=", project_id))
        if assignee_name:
            domain.append(("user_ids.name", "ilike", assignee_name))
        if stage:
            domain.append(("stage_id.name", "ilike", stage))
        if priority:
            domain.append(("priority", "=", priority))
        return client.search_read(
            "project.task", domain, TASK_FIELDS, limit=limit, offset=offset,
            order="priority desc, date_deadline asc",
        )

    @mcp.tool()
    def get_task(task_id: int) -> dict:
        """Get a specific task by ID.

        Args:
            task_id: The project.task record ID.
        """
        client = get_client()
        records = client.read("project.task", [task_id], TASK_FIELDS)
        if not records:
            return {"error": f"Task {task_id} not found"}
        return records[0]

    @mcp.tool()
    def create_task(
        name: str,
        project_id: int,
        description: str | None = None,
        user_ids: list[int] | None = None,
        date_deadline: str | None = None,
        planned_hours: float | None = None,
        priority: str = "0",
        parent_id: int | None = None,
    ) -> dict:
        """Create a new project task.

        Args:
            name: Task title.
            project_id: The project to add this task to.
            description: Task description/details.
            user_ids: List of user IDs to assign the task to.
            date_deadline: Deadline as 'YYYY-MM-DD'.
            planned_hours: Estimated hours for the task.
            priority: '0' for normal, '1' for important/urgent.
            parent_id: Parent task ID for sub-tasks.
        """
        client = get_client()
        values: dict[str, Any] = {
            "name": name,
            "project_id": project_id,
            "priority": priority,
        }
        if description:
            values["description"] = description
        if user_ids:
            values["user_ids"] = [(6, 0, user_ids)]
        if date_deadline:
            values["date_deadline"] = date_deadline
        if planned_hours is not None:
            values["planned_hours"] = planned_hours
        if parent_id:
            values["parent_id"] = parent_id

        new_id = client.create("project.task", values)
        return client.read("project.task", [new_id], TASK_FIELDS)[0]

    @mcp.tool()
    def update_task(task_id: int, values: dict) -> dict:
        """Update an existing project task.

        Args:
            task_id: The project.task record ID.
            values: Dict of field names to new values. Common fields:
                    name, description, priority, date_deadline, planned_hours, state.
        """
        client = get_client()
        client.write("project.task", [task_id], values)
        return client.read("project.task", [task_id], TASK_FIELDS)[0]
