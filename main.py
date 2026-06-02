from agents.planner_agent import PlannerAgent
from agents.supervisor_agent import SupervisorAgent

planner = PlannerAgent()
supervisor = SupervisorAgent()

while True:

    query = input("\nAsk a question or type 'exit': ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    plan = planner.create_plan(query)

    print("\nExecution Plan:")
    for step in plan["plan"]:
        print(f"- {step}")

    response = supervisor.handle_request(query)

    print("\nResponse:")
    print(response)