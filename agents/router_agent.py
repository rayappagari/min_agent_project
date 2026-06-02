from skills.cohort_analysis import skill as cohort_skill
from skills.inventory_analysis import skill as inventory_skill
from skills.financial_reporting import skill as financial_skill

skills = [
    cohort_skill,
    inventory_skill,
    financial_skill
]


class RouterAgent:

    def route(self, query: str):

        for skill in skills:

            if skill.matches(query):
                return skill

        return None