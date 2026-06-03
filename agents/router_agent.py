import os
from pathlib import Path
import anthropic

# Load .env if present
_env_path = Path(__file__).resolve().parents[1] / ".env"
if _env_path.exists():
    for _line in _env_path.read_text().splitlines():
        if "=" in _line and not _line.startswith("#"):
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
from skills.cohort_analysis import skill as cohort_skill
from skills.inventory_analysis import skill as inventory_skill
from skills.financial_reporting import skill as financial_skill

_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

_skills = [cohort_skill, inventory_skill, financial_skill]
_skill_map = {s.name: s for s in _skills}

_SKILLS_DESCRIPTION = "\n".join(
    f"- {s.name}: {s.description} (keywords: {', '.join(s.keywords)})"
    for s in _skills
)

_SYSTEM_PROMPT = f"""\
You are a routing agent for a business analytics assistant.

Given a user query, select the most appropriate skill from the list below.

Available skills:
{_SKILLS_DESCRIPTION}

Rules:
- Reply with ONLY the exact skill name (e.g. cohort_analysis).
- If no skill matches, reply with exactly: none
- Do not include any explanation or extra text.
"""


class RouterAgent:
    """Maps a natural-language query to a registered Skill via Claude.

    Claude selects the best matching skill from the registered list. Returns
    None if no skill matches, which causes SupervisorAgent to return a
    "No skill found" error to the user.

    To add a new domain: create a skill file in skills/, instantiate a Skill,
    and add it to _skills above.
    """

    def route(self, query: str):
        """Ask Claude to select the best matching Skill for the query.

        Args:
            query: Natural-language user input.

        Returns:
            Matching Skill instance, or None.
        """
        response = _client.messages.create(
            model="claude-opus-4-8",
            max_tokens=32,
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": query}],
        )

        skill_name = response.content[0].text.strip().lower()
        return _skill_map.get(skill_name)
