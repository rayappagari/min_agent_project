def before_tool(tool_name, payload):

    print(
        f"[HOOK] Calling {tool_name}"
    )

    print(
        f"[HOOK] Payload: {payload}"
    )


def after_tool(tool_name, result):

    print(
        f"[HOOK] {tool_name} completed"
    )

    print(
        f"[HOOK] Result: {result}"
    )