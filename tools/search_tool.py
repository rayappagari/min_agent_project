"""Search tool — keyword lookup against an in-memory knowledge base.

In production, this would perform vector search over a document store.
Currently matches the first keyword found in the query against a small
hardcoded dict of business metric definitions.
"""


def search_documents(query: str) -> str:
    """Return the definition for the first keyword found in the query.

    Iterates the knowledge base keys in insertion order and returns the value
    for the first key that appears as a substring in the query.

    Args:
        query: Natural-language question (e.g. "what is retention?").

    Returns:
        Matching definition string, or "No matching document found."
    """
    knowledge = {
        "retention":
            "Retention measures how many customers continue purchasing over time.",

        "inventory":
            "Inventory turns indicate how efficiently inventory is sold.",

        "revenue":
            "Revenue is the total income generated from sales."
    }

    query = query.lower()

    for keyword, value in knowledge.items():

        if keyword in query:
            return value

    return "No matching document found."
