def execute_sql(skill_name: str):
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