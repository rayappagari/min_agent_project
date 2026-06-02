from agents.router_agent import RouterAgent
from agents.sql_agent import SQLAgent
from agents.rag_agent import RAGAgent
from memory.session_memory import SessionMemory


class SupervisorAgent:
    """Central dispatcher that routes every user query to the correct agent.

    Routing rules applied in order:
    1. Follow-up detection — "compare with last month" rewrites the query
       using the last metric query from SessionMemory before re-routing.
    2. Definition routing — "what is" / "explain" → RAGAgent.
    3. Metric routing — all other queries → RouterAgent → SQLAgent.

    Every query and response is saved to SessionMemory for follow-up support.
    """

    def __init__(self):
        self.router = RouterAgent()
        self.sql_agent = SQLAgent()
        self.rag_agent = RAGAgent()
        self.memory = SessionMemory()

    def handle_request(self, query: str) -> dict:
        """Route the query to the appropriate agent and return its response.

        Args:
            query: Natural-language user input (post HITL approval).

        Returns:
            Agent response dict, or {"error": str} if routing fails.
        """
        query_lower = query.lower()

        self.memory.add("user", query)

        # Rewrite follow-up comparisons using the last metric query from memory.
        if "compare with last month" in query_lower:

            last_query = self.memory.last_metric_query()

            if last_query:
                query = f"{last_query} and compare with last month"
                query_lower = query.lower()
            else:
                return {
                    "error": "Please ask a metric question first before comparing."
                }

        # Definition/explanation questions go straight to RAGAgent.
        if "what is" in query_lower or "explain" in query_lower:

            response = self.rag_agent.handle(query)
            self.memory.add("assistant", response)
            return response

        # All other queries are matched to a skill and executed via SQLAgent.
        skill = self.router.route(query)

        if not skill:
            response = {"error": "No skill found"}
            self.memory.add("assistant", response)
            return response

        response = self.sql_agent.handle(skill.name)
        self.memory.add("assistant", response)
        return response
