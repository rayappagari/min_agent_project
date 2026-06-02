from mcp.server import MCPServer


class MCPClient:

    def __init__(self):
        self.server = MCPServer()

    def call_tool(
        self,
        tool_name,
        payload
    ):

        return self.server.execute_tool(
            tool_name,
            payload
        )