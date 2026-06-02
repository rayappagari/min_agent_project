class SessionMemory:

    def __init__(self):
        self.history = []

    def add(self, role, content):

        self.history.append({
            "role": role,
            "content": content
        })

    def get_history(self):

        return self.history

    def last_user_query(self):

        for item in reversed(self.history):

            if item["role"] == "user":
                return item["content"]

        return None

    def last_metric_query(self):

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