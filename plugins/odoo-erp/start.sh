#!/usr/bin/env bash
echo "Starting Odoo MCP Server on http://localhost:8000/mcp ..."
uv run --project . python -m src.server --http
