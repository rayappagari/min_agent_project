# min_agent_project

A minimal multi-agent system for answering business analytics queries using a planner/supervisor/router pipeline.

## Overview

Natural language queries are routed to one of two agents:

- **RAGAgent** — answers definition/explanation questions ("what is retention?") via keyword document lookup
- **SQLAgent** — executes mock SQL for metric queries (retention, inventory, financials) by matching a skill

The system also supports session-aware follow-ups like "compare with last month."

## Project Structure

```
agents/       # Planner, Supervisor, Router, SQL, RAG agents
skills/       # Domain skill definitions (cohort, inventory, financial)
tools/        # SQL and document search tool implementations (mocked)
mcp/          # In-process MCP client/server layer
memory/       # In-session conversation history
hooks/        # before/after tool logging hooks
evals/        # Routing eval suite
```

## Usage

```bash
python main.py
```

Example queries:
- `show customer retention`
- `what is inventory turns?`
- `show revenue by region`
- `compare with last month`

## Running Evals

```bash
python -m evals.test_routing
```
