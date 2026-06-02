class PlannerAgent:

    def create_plan(self, query: str):

        query_lower = query.lower()

        steps = []

        if "what is" in query_lower or "explain" in query_lower:
            steps.append("Use RAGAgent to retrieve definition/context")

        if any(word in query_lower for word in ["show", "calculate", "compare", "trend"]):
            steps.append("Use SQLAgent to retrieve metric/result")

        if not steps:
            steps.append("Use SupervisorAgent to determine best route")

        return {
            "query": query,
            "plan": steps
        }