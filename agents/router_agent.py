from skills.cohort_analysis import skill as cohort_skill
from skills.inventory_analysis import skill as inventory_skill
from skills.financial_reporting import skill as financial_skill

# Skills are evaluated in registration order; first match wins.
skills = [
    cohort_skill,
    inventory_skill,
    financial_skill
]


class RouterAgent:
    """Maps a natural-language query to a registered Skill via keyword matching.

    Skills are checked in order. The first skill whose keywords appear in the
    query is returned. Returns None if no skill matches, which causes
    SupervisorAgent to return a "No skill found" error to the user.

    To add a new domain: create a skill file in skills/, instantiate a Skill,
    and append it to the skills list above.
    """

    def route(self, query: str):
        """Return the first Skill whose keywords match the query, or None.

        Args:
            query: Natural-language user input (case-insensitive matching).

        Returns:
            Matching Skill instance, or None.
        """
        for skill in skills:

            if skill.matches(query):
                return skill

        return None
