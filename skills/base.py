from dataclasses import dataclass
from typing import List


@dataclass
class Skill:
    """Describes a business analytics domain and how to recognise queries for it.

    Attributes:
        name: Unique identifier used as the key for SQL tool dispatch.
        description: Human-readable label for the skill.
        keywords: Strings that, if found in a query, activate this skill.
    """

    name: str
    description: str
    keywords: List[str]

    def matches(self, query: str) -> bool:
        """Return True if any keyword appears in the query (case-insensitive).

        Args:
            query: Natural-language user input.
        """
        query = query.lower()

        return any(
            keyword.lower() in query
            for keyword in self.keywords
        )
