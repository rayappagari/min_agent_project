from agents.router_agent import RouterAgent
from agents.sql_agent import SQLAgent
from agents.rag_agent import RAGAgent
from memory.session_memory import SessionMemory


class SupervisorAgent:

    def __init__(self):

        self.router = RouterAgent()
        self.sql_agent = SQLAgent()
        self.rag_agent = RAGAgent()
        self.memory = SessionMemory()

    def handle_request(self, query):

        query_lower = query.lower()

        # Save user query into memory
        self.memory.add("user", query)

        # If user asks a follow-up like "compare with last month"
        if "compare with last month" in query_lower:

            last_query = self.memory.last_metric_query()

            if last_query:
                query = f"{last_query} and compare with last month"
                query_lower = query.lower()
            else:
                return {
                    "error": "Please ask a metric question first before comparing."
                }

        # Route definition/explanation questions to RAG Agent
        if "what is" in query_lower or "explain" in query_lower:

            response = self.rag_agent.handle(query)

            self.memory.add("assistant", response)

            return response

        # Route metric questions to SQL Agent
        skill = self.router.route(query)

        if not skill:
            response = {
                "error": "No skill found"
            }

            self.memory.add("assistant", response)

            return response

        response = self.sql_agent.handle(skill.name)

        self.memory.add("assistant", response)

        return response