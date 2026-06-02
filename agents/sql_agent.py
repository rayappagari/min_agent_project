from mcp.client import MCPClient

class SQLAgent:

    def __init__(self):
        self.mcp = MCPClient()

    def handle(self, skill_name):

        response = self.mcp.call_tool(
            "execute_sql",
            skill_name
        )

        return {
            "agent": "sql_agent",
            "sql": response["sql"],
            "result": response["result"]
        }