from mcp.client import MCPClient

class RAGAgent:

    def __init__(self):
        self.mcp = MCPClient()

    def handle(self, query):

        result = self.mcp.call_tool(
            "search_documents",
            query
        )

        return {
            "agent": "rag_agent",
            "answer": result
        }