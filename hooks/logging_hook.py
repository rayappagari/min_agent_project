"""Lifecycle hooks executed by MCPServer before and after every tool call.

Extend these functions to add cross-cutting behaviour such as latency
tracking, audit logging, or input/output validation without modifying
individual tool implementations.
"""


def before_tool(tool_name: str, payload) -> None:
    """Log the tool name and payload before execution begins.

    Args:
        tool_name: Name of the tool about to be called.
        payload: Input data being passed to the tool.
    """
    print(f"[HOOK] Calling {tool_name}")
    print(f"[HOOK] Payload: {payload}")


def after_tool(tool_name: str, result) -> None:
    """Log the tool name and result after execution completes.

    Args:
        tool_name: Name of the tool that just ran.
        result: Output returned by the tool.
    """
    print(f"[HOOK] {tool_name} completed")
    print(f"[HOOK] Result: {result}")
