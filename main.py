from agents.planner_agent import PlannerAgent
from agents.supervisor_agent import SupervisorAgent

planner = PlannerAgent()
supervisor = SupervisorAgent()

while True:

    query = input("\nAsk a question or type 'exit': ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    while True:
        plan = planner.create_plan(query)

        print("\nExecution Plan:")
        for step in plan["plan"]:
            print(f"- {step}")

        approval = input("\nProceed? (yes / no / edit): ").strip().lower()

        if approval in ("yes", "y"):
            break
        elif approval in ("no", "n"):
            print("Cancelled.")
            query = None
            break
        elif approval == "edit":
            query = input("Enter revised query: ").strip()
        else:
            print("Please enter yes, no, or edit.")

    if not query:
        continue

    response = supervisor.handle_request(query)

    print("\nResponse:")
    print(response)
