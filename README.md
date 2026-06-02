# min_agent_project

A minimal but complete multi-agent system for answering business analytics queries in natural language. Designed as a learning reference for agentic architecture patterns: planning, routing, tool use, memory, and hooks.

---

## Agentic Architecture Overview

```
User Input (natural language)
        │
        ▼
  PlannerAgent          ← generates a human-readable execution plan (display only)
        │
        ▼
  SupervisorAgent       ← central dispatcher; owns all routing logic
     │        │
     ▼        ▼
 RAGAgent   SQLAgent    ← specialized agents for different query types
               │
               ▼
          RouterAgent   ← maps query to a domain Skill
               │
               ▼
           MCPClient
               │
               ▼
           MCPServer    ← tool registry with before/after hooks
               │
               ▼
        sql_tool / search_tool   ← leaf-level tool implementations
```

There are two parallel flows triggered for every user query:

1. **Plan flow** (`PlannerAgent`) — generates a printed plan for transparency, but does not control execution.
2. **Execution flow** (`SupervisorAgent` → agents → tools) — actually resolves the query.

---

## Components

### 1. PlannerAgent (`agents/planner_agent.py`)

Inspects the query with keyword rules and returns a list of steps describing what *should* happen. This plan is shown to the user but is **not** passed to `SupervisorAgent` — the two flows are independent.

**Input:** raw user query string  
**Output:** `{ "query": str, "plan": [str, ...] }`

**Example:**
```python
planner.create_plan("show revenue by region")
# → { "query": "show revenue by region", "plan": ["Use SQLAgent to retrieve metric/result"] }

planner.create_plan("what is retention?")
# → { "query": "what is retention?", "plan": ["Use RAGAgent to retrieve definition/context"] }
```

The planner covers three patterns:
- `"what is"` / `"explain"` → RAG step
- `"show"` / `"calculate"` / `"compare"` / `"trend"` → SQL step
- Anything else → fallback "Use SupervisorAgent to determine best route"

---

### 2. SupervisorAgent (`agents/supervisor_agent.py`)

The central dispatcher. Every query passes through here. It applies three routing rules in order:

1. **Follow-up detection** — if the query contains `"compare with last month"`, it looks up the last metric query from `SessionMemory` and rewrites the query before continuing.
2. **Definition routing** — if the query contains `"what is"` or `"explain"`, it delegates to `RAGAgent`.
3. **Metric routing** — everything else is passed to `RouterAgent` to find a matching `Skill`, then forwarded to `SQLAgent`.

**Example — definition query:**
```python
supervisor.handle_request("what is churn?")
# → RAGAgent.handle("what is churn?")
# → { "agent": "rag_agent", "answer": "Retention measures how many customers..." }
```

**Example — metric query:**
```python
supervisor.handle_request("show inventory turns")
# → RouterAgent.route("show inventory turns") → inventory_analysis skill
# → SQLAgent.handle("inventory_analysis")
# → { "agent": "sql_agent", "sql": "SELECT ...", "result": "Inventory Turns = 11.2" }
```

**Example — follow-up query:**
```python
supervisor.handle_request("show revenue by region")   # first query
supervisor.handle_request("compare with last month")  # follow-up
# Memory rewrites to: "show revenue by region and compare with last month"
# → routed as a metric query
```

All queries and responses are saved to `SessionMemory` before returning.

---

### 3. RouterAgent (`agents/router_agent.py`)

Iterates a static list of registered `Skill` objects and returns the first one whose keywords match the query. Returns `None` if no skill matches.

**Registered skills (in order):**
1. `cohort_analysis`
2. `inventory_analysis`
3. `financial_reporting`

**Example:**
```python
router.route("calculate stockout risk")
# Checks cohort_analysis keywords: ["retention", "cohort", "churn", "funnel", "conversion"] → no match
# Checks inventory_analysis keywords: ["inventory", "stock", "doh", "stockout", "warehouse", "fill rate"] → "stockout" matches
# → returns inventory_analysis Skill
```

**Order matters** — the first matching skill wins. If two skills share a keyword, the one registered earlier takes priority.

---

### 4. SQLAgent (`agents/sql_agent.py`)

Receives a skill name and delegates to the MCP layer to execute a SQL query. Returns the generated SQL and the result.

**Input:** skill name string (e.g. `"financial_reporting"`)  
**Output:** `{ "agent": "sql_agent", "sql": str, "result": str }`

```python
sql_agent.handle("cohort_analysis")
# → MCPClient.call_tool("execute_sql", "cohort_analysis")
# → { "agent": "sql_agent",
#     "sql": "SELECT cohort_month, retention_rate FROM customer_retention...",
#     "result": "Retention Rate = 82%" }
```

---

### 5. RAGAgent (`agents/rag_agent.py`)

Handles natural language definition/explanation queries. Delegates to the MCP layer to search a small in-memory knowledge base.

**Input:** raw query string  
**Output:** `{ "agent": "rag_agent", "answer": str }`

```python
rag_agent.handle("what is inventory turns?")
# → MCPClient.call_tool("search_documents", "what is inventory turns?")
# → { "agent": "rag_agent", "answer": "Inventory turns indicate how efficiently inventory is sold." }
```

---

## Skills (`skills/`)

A `Skill` (defined in `skills/base.py`) is a dataclass that describes a business domain with:
- `name` — unique identifier used as the key for SQL dispatch
- `description` — human-readable label
- `keywords` — list of strings; matching is case-insensitive substring search

```python
@dataclass
class Skill:
    name: str
    description: str
    keywords: List[str]

    def matches(self, query: str) -> bool:
        return any(keyword.lower() in query.lower() for keyword in self.keywords)
```

**Current skills:**

| Skill | Keywords |
|---|---|
| `cohort_analysis` | retention, cohort, churn, funnel, conversion |
| `inventory_analysis` | inventory, stock, doh, stockout, warehouse, fill rate |
| `financial_reporting` | revenue, sales, profit, margin, financial |

**Adding a new skill** — create a file in `skills/`, instantiate a `Skill`, then add it to the list in `agents/router_agent.py`:

```python
# skills/customer_support.py
from skills.base import Skill
skill = Skill(
    name="customer_support",
    description="Support ticket and resolution metrics",
    keywords=["ticket", "resolution", "csat", "nps"]
)

# agents/router_agent.py
from skills.customer_support import skill as support_skill
skills = [cohort_skill, inventory_skill, financial_skill, support_skill]
```

---

## MCP Layer (`mcp/`)

The Model Context Protocol (MCP) layer provides a clean client/server boundary between agents and tools, even though both run in-process here.

### MCPClient (`mcp/client.py`)

Thin wrapper that forwards `call_tool(tool_name, payload)` to `MCPServer`.

```python
client = MCPClient()
client.call_tool("execute_sql", "financial_reporting")
# → MCPServer.execute_tool("execute_sql", "financial_reporting")
```

### MCPServer (`mcp/server.py`)

The tool registry and execution engine. Dispatches by `tool_name`, wraps execution with lifecycle hooks.

```python
def execute_tool(self, tool_name, payload):
    before_tool(tool_name, payload)    # logging hook fires first

    if tool_name == "execute_sql":
        result = execute_sql(payload)
    elif tool_name == "search_documents":
        result = search_documents(payload)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

    after_tool(tool_name, result)      # logging hook fires after
    return result
```

To register a new tool: add a branch in `execute_tool` and implement the function in `tools/`.

---

## Tools (`tools/`)

Leaf-level implementations called by `MCPServer`. Currently mocked with hardcoded data.

### sql_tool (`tools/sql_tool.py`)

Maps a skill name to a SQL string and a mock result.

```python
execute_sql("financial_reporting")
# → {
#     "sql": "SELECT region, SUM(revenue) AS revenue FROM sales GROUP BY region;",
#     "result": "Revenue = $12.5M"
#   }
```

### search_tool (`tools/search_tool.py`)

Keyword-scans a small in-memory knowledge dict and returns the first matching definition.

```python
search_documents("what is retention?")
# → "Retention measures how many customers continue purchasing over time."

search_documents("what is margin?")
# → "No matching document found."
```

---

## Memory (`memory/session_memory.py`)

`SessionMemory` is an in-process conversation log. It stores `{ role, content }` entries and provides two retrieval helpers:

- `last_user_query()` — most recent user turn
- `last_metric_query()` — most recent user turn that contains a metric keyword (used for "compare with last month")

```python
memory = SessionMemory()
memory.add("user", "show revenue by region")
memory.add("assistant", { "agent": "sql_agent", "result": "Revenue = $12.5M" })

memory.last_metric_query()
# → "show revenue by region"   (matched on "revenue")
```

Memory is **ephemeral** — it resets each time `main.py` is restarted. There is no persistence layer.

---

## Hooks (`hooks/logging_hook.py`)

Hooks are plain functions called by `MCPServer` before and after every tool execution. They currently print to stdout.

```python
# Console output for: sql_agent.handle("cohort_analysis")
[HOOK] Calling execute_sql
[HOOK] Payload: cohort_analysis
[HOOK] execute_sql completed
[HOOK] Result: { "sql": "...", "result": "Retention Rate = 82%" }
```

To add behavior (e.g. latency tracking, audit logging), extend `before_tool` / `after_tool` in `hooks/logging_hook.py`.

---

## Evals (`evals/test_routing.py`)

A plain Python script (not a test framework) that runs routing assertions and prints `PASS`/`FAIL`. Run from the project root:

```bash
python -m evals.test_routing
```

**Output:**
```
PASS: show customer retention
PASS: show inventory turns
PASS: show revenue by region
PASS: calculate stockout risk

Passed 4/4 tests
```

Each test case is a dict with `query` and `expected_skill`. Add new cases to the `test_cases` list to cover additional routing scenarios.

---

## Running

```bash
python main.py
```

**Sample session:**
```
Ask a question or type 'exit': show inventory turns

Execution Plan:
- Use SQLAgent to retrieve metric/result

Response:
{'agent': 'sql_agent', 'sql': '\nSELECT warehouse_id,\n       inventory_turns,\n       stockout_risk\nFROM inventory_metrics;\n', 'result': 'Inventory Turns = 11.2'}

Ask a question or type 'exit': what is retention?

Execution Plan:
- Use RAGAgent to retrieve definition/context

Response:
{'agent': 'rag_agent', 'answer': 'Retention measures how many customers continue purchasing over time.'}
```
