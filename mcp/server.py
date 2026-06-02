from tools.sql_tool import execute_sql
from tools.search_tool import search_documents

from hooks.logging_hook import (
    before_tool,
    after_tool
)


class MCPServer:
    """Tool registry and execution engine for the MCP layer.

    Dispatches tool calls by name, wraps each execution with before/after
    lifecycle hooks, and raises ValueError for unregistered tool names.

    To register a new tool: add an elif branch in execute_tool and implement
    the function in tools/.
    """

    def execute_tool(self, tool_name: str, payload) -> dict:
        """Dispatch a tool call, run lifecycle hooks, and return the result.

        Args:
            tool_name: Registered tool name ("execute_sql" or
                       "search_documents").
            payload: Forwarded directly to the tool function.

        Returns:
            Tool result.

        Raises:
            ValueError: If tool_name is not registered.
        """
        before_tool(tool_name, payload)

        if tool_name == "execute_sql":
            result = execute_sql(payload)
        elif tool_name == "search_documents":
            result = search_documents(payload)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

        after_tool(tool_name, result)

        return result
