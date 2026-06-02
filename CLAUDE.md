# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

Install dependencies:
```
pip install -r requirements.txt
```

Set your Anthropic API key (required — PlannerAgent and RouterAgent call Claude):
```
export ANTHROPIC_API_KEY=your-key-here   # Linux/macOS
$env:ANTHROPIC_API_KEY = "your-key-here" # PowerShell
```

## Commands

Run the interactive assistant:
```
python main.py
```

Run the routing eval suite:
```
python -m evals.test_routing
```

## Architecture

This is a minimal multi-agent system for answering business analytics queries (retention, inventory, financial). The request flow is:

```
main.py
  → PlannerAgent       — generates a human-readable plan (display only, not used for routing)
  → SupervisorAgent    — actual routing logic
      ├─ RAGAgent       — handles "what is" / "explain" queries via keyword doc lookup
      └─ SQLAgent       — handles metric queries; delegates to RouterAgent first
           └─ RouterAgent → matches query to a Skill by keyword → SQLAgent executes via MCP
```

**SupervisorAgent** (`agents/supervisor_agent.py`) is the central dispatcher. It hard-codes two routing rules before delegating to `RouterAgent`: definition questions go to `RAGAgent`, and "compare with last month" triggers a memory lookup to reconstruct the prior metric query.

**Skills** (`skills/`) are plain dataclasses (`Skill` from `skills/base.py`) with a `name`, `description`, and `keywords` list. `RouterAgent` iterates registered skills and returns the first whose keywords match the query. To add a new domain, create a skill file, instantiate a `Skill`, and add it to the list in `agents/router_agent.py`.

**MCP layer** (`mcp/`) simulates a client/server boundary in-process. `MCPClient.call_tool` calls `MCPServer.execute_tool`, which dispatches to either `tools/sql_tool.py` or `tools/search_tool.py`. All tool implementations are currently mocked with hardcoded data.

**Human-in-the-loop gate** (`main.py`) — sits between `PlannerAgent` and `SupervisorAgent`. After the plan is printed, the user must type `yes` to execute, `no` to cancel, or `edit` to revise the query (which re-plans and re-asks). No agent or tool runs until the user approves. When editing, the loop reruns `planner.create_plan()` on the new query before asking again.

**Hooks** (`hooks/logging_hook.py`) provide `before_tool` / `after_tool` callbacks.

**SessionMemory** (`memory/session_memory.py`) stores the conversation history in-process (lost on restart). `last_metric_query()` scans history in reverse for the most recent user turn containing a metric keyword — used by the "compare with last month" feature.

**Evals** (`evals/test_routing.py`) are plain Python scripts with manual `PASS`/`FAIL` output — not a test framework. Run directly with `python`.
