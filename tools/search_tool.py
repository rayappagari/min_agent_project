def search_documents(query):

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