from tools.sql_tool import execute_sql
from tools.search_tool import search_documents

from hooks.logging_hook import (
    before_tool,
    after_tool
)


class MCPServer:

    def execute_tool(self, tool_name, payload):
        before_tool(tool_name, payload)

        if tool_name == "execute_sql":
            result = execute_sql(payload)
        elif tool_name == "search_documents":
            result = search_documents(payload)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

        after_tool(tool_name, result)

        return result