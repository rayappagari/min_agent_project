from agents.router_agent import RouterAgent

test_cases = [
    # cohort_analysis
    {
        "query": "show customer retention",
        "expected_skill": "cohort_analysis"
    },
    {
        "query": "calculate churn rate this quarter",
        "expected_skill": "cohort_analysis"
    },
    {
        "query": "show cohort breakdown by signup month",
        "expected_skill": "cohort_analysis"
    },
    {
        "query": "what is the funnel drop-off rate?",
        "expected_skill": "cohort_analysis"
    },
    {
        "query": "show conversion rate by campaign",
        "expected_skill": "cohort_analysis"
    },

    # inventory_analysis
    {
        "query": "show inventory turns",
        "expected_skill": "inventory_analysis"
    },
    {
        "query": "calculate stockout risk",
        "expected_skill": "inventory_analysis"
    },
    {
        "query": "show current stock levels",
        "expected_skill": "inventory_analysis"
    },
    {
        "query": "show days on hand by SKU",
        "expected_skill": "inventory_analysis"
    },
    {
        "query": "calculate fill rate by warehouse",
        "expected_skill": "inventory_analysis"
    },

    # financial_reporting
    {
        "query": "show revenue by region",
        "expected_skill": "financial_reporting"
    },
    {
        "query": "show total sales last month",
        "expected_skill": "financial_reporting"
    },
    {
        "query": "calculate profit by product line",
        "expected_skill": "financial_reporting"
    },
    {
        "query": "show gross margin trend",
        "expected_skill": "financial_reporting"
    },
    {
        "query": "show financial summary for Q1",
        "expected_skill": "financial_reporting"
    },

    # no match
    {
        "query": "hello there",
        "expected_skill": None
    },
    {
        "query": "what time is it?",
        "expected_skill": None
    },
]

router = RouterAgent()

passed = 0

for test in test_cases:
    skill = router.route(test["query"])

    actual = skill.name if skill else None

    if actual == test["expected_skill"]:
        print(f"PASS: {test['query']}")
        passed += 1
    else:
        print(
            f"FAIL: {test['query']} "
            f"expected={test['expected_skill']} actual={actual}"
        )

print(f"\nPassed {passed}/{len(test_cases)} tests")