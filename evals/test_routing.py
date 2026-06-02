from agents.router_agent import RouterAgent

test_cases = [
    {
        "query": "show customer retention",
        "expected_skill": "cohort_analysis"
    },
    {
        "query": "show inventory turns",
        "expected_skill": "inventory_analysis"
    },
    {
        "query": "show revenue by region",
        "expected_skill": "financial_reporting"
    },
    {
        "query": "calculate stockout risk",
        "expected_skill": "inventory_analysis"
    }
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