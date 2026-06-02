class PlannerAgent:
    """Inspects a user query and produces a human-readable execution plan.

    The plan is displayed to the user before the HITL approval gate but is
    not passed to SupervisorAgent — planning and execution are independent.
    """

    def create_plan(self, query: str) -> dict:
        """Return a plan dict describing which agent(s) should handle the query.

        Matches against keyword patterns in order:
        - "what is" / "explain" → RAGAgent step
        - "show" / "calculate" / "compare" / "trend" → SQLAgent step
        - No match → generic SupervisorAgent fallback step

        Args:
            query: Raw natural-language user input.

        Returns:
            {"query": str, "plan": [str, ...]}
        """
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
