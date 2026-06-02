from mcp.client import MCPClient


class SQLAgent:
    """Executes a SQL query for a matched skill via the MCP layer.

    Receives a skill name from SupervisorAgent, delegates to MCPClient
    which calls the execute_sql tool, and returns the SQL and result.
    """

    def __init__(self):
        self.mcp = MCPClient()

    def handle(self, skill_name: str) -> dict:
        """Invoke the execute_sql tool for the given skill and return results.

        Args:
            skill_name: The Skill.name string (e.g. "inventory_analysis").

        Returns:
            {"agent": "sql_agent", "sql": str, "result": str}
        """
        response = self.mcp.call_tool(
            "execute_sql",
            skill_name
        )

        return {
            "agent": "sql_agent",
            "sql": response["sql"],
            "result": response["result"]
        }
