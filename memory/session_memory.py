class SessionMemory:
    """In-process conversation log for a single session.

    Stores a flat list of {"role", "content"} turns. Used by SupervisorAgent
    to support follow-up queries like "compare with last month".

    Memory is ephemeral — it resets when the process restarts.
    """

    def __init__(self):
        self.history = []

    def add(self, role: str, content) -> None:
        """Append a turn to the conversation history.

        Args:
            role: "user" or "assistant".
            content: Query string (user) or response dict (assistant).
        """
        self.history.append({
            "role": role,
            "content": content
        })

    def get_history(self) -> list:
        """Return the full conversation history."""
        return self.history

    def last_user_query(self) -> str | None:
        """Return the most recent user turn, or None if history is empty."""
        for item in reversed(self.history):

            if item["role"] == "user":
                return item["content"]

        return None

    def last_metric_query(self) -> str | None:
        """Return the most recent user query containing a metric keyword.

        Scans history in reverse and returns the first user turn that contains
        any of the known metric keywords. Used to reconstruct context for
        "compare with last month" follow-ups.

        Returns:
            Matching query string, or None if no metric query exists yet.
        """
        metric_keywords = [
            "inventory",
            "stock",
            "revenue",
            "sales",
            "profit",
            "margin",
            "retention",
            "cohort",
            "churn",
            "warehouse"
        ]

        for item in reversed(self.history):

            if item["role"] != "user":
                continue

            query = item["content"].lower()

            if any(
                keyword in query
                for keyword in metric_keywords
            ):
                return item["content"]

        return None
