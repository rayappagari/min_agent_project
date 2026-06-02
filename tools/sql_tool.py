"""SQL tool — maps a skill name to a mock SQL query and result.

In production, this would build and execute a real SQL query against a
database. Currently returns hardcoded queries and results for each skill.
"""


def execute_sql(skill_name: str) -> dict:
    """Return the SQL query and result for the given skill.

    Args:
        skill_name: One of "cohort_analysis", "inventory_analysis",
                    or "financial_reporting".

    Returns:
        {"sql": str, "result": str}. Falls back to placeholder strings
        if skill_name is not recognised.
    """
    mock_queries = {
        "cohort_analysis": """
SELECT cohort_month,
       retention_rate
FROM customer_retention
ORDER BY cohort_month;
""",
        "inventory_analysis": """
SELECT warehouse_id,
       inventory_turns,
       stockout_risk
FROM inventory_metrics;
""",
        "financial_reporting": """
SELECT region,
       SUM(revenue) AS revenue
FROM sales
GROUP BY region;
"""
    }

    mock_results = {
        "cohort_analysis": "Retention Rate = 82%",
        "inventory_analysis": "Inventory Turns = 11.2",
        "financial_reporting": "Revenue = $12.5M"
    }

    return {
        "sql": mock_queries.get(skill_name, "No SQL generated"),
        "result": mock_results.get(skill_name, "No data found")
    }
