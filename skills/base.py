from dataclasses import dataclass
from typing import List

@dataclass
class Skill:
    name: str
    description: str
    keywords: List[str]

    def matches(self, query: str) -> bool:
        query = query.lower()

        return any(
            keyword.lower() in query
            for keyword in self.keywords
        )