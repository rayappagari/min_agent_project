from mcp.client import MCPClient


class RAGAgent:
    """Answers definition and explanation queries via document search.

    Delegates to the search_documents tool through the MCP layer. The tool
    performs keyword lookup against an in-memory knowledge base and returns
    the first matching definition.
    """

    def __init__(self):
        self.mcp = MCPClient()

    def handle(self, query: str) -> dict:
        """Search the knowledge base for a definition matching the query.

        Args:
            query: Natural-language question (e.g. "what is retention?").

        Returns:
            {"agent": "rag_agent", "answer": str}
        """
        result = self.mcp.call_tool(
            "search_documents",
            query
        )

        return {
            "agent": "rag_agent",
            "answer": result
        }
