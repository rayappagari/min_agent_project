from mcp.server import MCPServer


class MCPClient:
    """Thin client that forwards tool calls to MCPServer.

    Provides a clean boundary between agents and tool implementations.
    In production this boundary would be a network call; here it is in-process.
    """

    def __init__(self):
        self.server = MCPServer()

    def call_tool(self, tool_name: str, payload) -> dict:
        """Forward a tool call to MCPServer and return the result.

        Args:
            tool_name: Name of the registered tool ("execute_sql" or
                       "search_documents").
            payload: Data passed to the tool (skill name or query string).

        Returns:
            Tool result dict as returned by MCPServer.
        """
        return self.server.execute_tool(
            tool_name,
            payload
        )
