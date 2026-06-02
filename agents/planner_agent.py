import os
import anthropic

_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

_SYSTEM_PROMPT = """\
You are a planning agent for a business analytics assistant.

Given a user query, output a concise execution plan as a numbered list of steps.
Each step must name the specific agent to use:
- RAGAgent — for definitions and explanations ("what is X", "explain Y")
- SQLAgent — for metric queries (show, calculate, compare, trend)

Rules:
- Output only the steps, one per line, no preamble or explanation.
- If the query fits neither, output a single step: "Use SupervisorAgent to determine best route"

Example:
Query: "show revenue by region"
Steps:
1. Use SQLAgent to retrieve metric/result

Example:
Query: "what is churn?"
Steps:
1. Use RAGAgent to retrieve definition/context
"""


class PlannerAgent:
    """Inspects a user query via Claude and produces a human-readable execution plan.

    The plan is displayed to the user before the HITL approval gate but is
    not passed to SupervisorAgent — planning and execution are independent.
    """

    def create_plan(self, query: str) -> dict:
        """Call Claude to generate a plan for the given query.

        Args:
            query: Raw natural-language user input.

        Returns:
            {"query": str, "plan": [str, ...]}
        """
        response = _client.messages.create(
            model="claude-opus-4-8",
            max_tokens=256,
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": f"Query: {query}"}],
        )

        text = response.content[0].text.strip()
        steps = [
            line.lstrip("0123456789.-) ").strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return {
            "query": query,
            "plan": steps,
        }
