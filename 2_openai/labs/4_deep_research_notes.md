# Daily Learning & Practice Notes — `4_deep_research.ipynb` (ignore creds)

This lab builds a classic “deep research” agentic workflow:

- plan searches (structured output)
- execute multiple web searches (tool use + async parallelism)
- synthesize a long-form report (structured output)
- optionally email the report (tool use)

---

## What you build (high level)

An end-to-end pipeline:

1. **PlannerAgent** proposes \(N\) targeted web searches (as a structured plan)
2. **Search agent** runs web searches and returns short summaries
3. **WriterAgent** produces a detailed markdown report (plus summary + follow-ups)
4. **Email agent** sends the report (optional side-effect)
5. Everything runs under `trace(...)` so you can debug the workflow

---

## Definitions (learn these first)

### Hosted tools (concept)

The Agents SDK can provide “hosted tools” (tools managed by the platform). In this notebook, you use:

- **`WebSearchTool`**: lets an agent search the web and incorporate results into its response.

Key idea: a hosted tool is a **capability** the model can invoke; you guide that invocation using agent instructions + model settings.

### Core Agents SDK pieces

- **`Agent`**: a role with `instructions`, optional `tools`, optional structured `output_type`.
- **`Runner.run(agent, input)`**: executes one agent run; result is `result.final_output`.
- **`trace("name")`**: captures observability data for the whole workflow (agent steps, tool calls, errors).

### Model settings (tool control)

- **`ModelSettings(tool_choice="required")`**: forces the model to call a tool when tools are available.
  - In this lab, it helps ensure the search agent actually uses `WebSearchTool` instead of “making up” a summary.

### Structured outputs (Pydantic)

Using `output_type=...` on an agent makes its final output a typed object:

- **`WebSearchPlan`**: list of planned searches (each with `query` + `reason`)
- **`ReportData`**: a report bundle:
  - `short_summary`
  - `markdown_report`
  - `follow_up_questions`

Why it matters: structured outputs reduce parsing hacks and make orchestration more reliable.

### Async concurrency

- **`asyncio.create_task(...)` + `asyncio.gather(...)`**: run multiple searches concurrently to reduce end-to-end latency.

---

## Notebook walkthrough (cell-by-cell)

### Markdown intro

Sets the context: “Deep Research” is a common cross-business agent use case.

### Imports + `.env`

Imports Agents SDK + Pydantic + async utilities + email helpers.  
Per your request: **ignore credential setup** — focus on the workflow mechanics.

### Hosted tools section (markdown)

Explains hosted tools available in the SDK and introduces `WebSearchTool` conceptually.

### Search agent (single-search summarizer)

You define:

- `search_agent = Agent(..., tools=[WebSearchTool(search_context_size="low")], model_settings=ModelSettings(tool_choice="required"))`

Important behavior:

- The agent is forced to call the web search tool (because tool choice is required).
- Output is a concise 2–3 paragraph summary (<300 words).

### Quick demo run (Search)

Runs:

- `await Runner.run(search_agent, "Latest AI Agent frameworks in 2025")`
- displays markdown output via `display(Markdown(...))`

Purpose:

- sanity check: tool works, outputs are usable as “research snippets”.

### PlannerAgent (structured plan)

You define:

- `HOW_MANY_SEARCHES = 3`
- Pydantic models `WebSearchItem` and `WebSearchPlan`
- `planner_agent = Agent(..., output_type=WebSearchPlan)`

Run:

- `result.final_output.searches` returns a typed list of search items.

Key idea:

- separate “what to search” (planning) from “doing searches” (execution).

### Email tool + Email agent (optional side-effect)

You define:

- a `@function_tool` `send_email(subject, html_body)` (SendGrid)
- `email_agent` whose only job is: convert report → clean HTML + subject, then call `send_email`

Even if you don’t actually send, this pattern is important:

- make side effects happen only through explicit tools.

### WriterAgent (structured report)

You define:

- `ReportData` schema (summary, markdown report, follow-ups)
- `writer_agent = Agent(..., output_type=ReportData)`

Writer instructions:

- first produce an outline (implicitly)
- generate a long markdown report (5–10 pages / 1000+ words)

### Orchestration functions (the real “workflow”)

The notebook then builds a small async pipeline:

- `plan_searches(query)`: calls PlannerAgent, returns `WebSearchPlan`
- `perform_searches(search_plan)`: runs all searches concurrently
- `search(item)`: uses Search agent to produce a summary per planned query
- `write_report(query, search_results)`: calls WriterAgent, returns `ReportData`
- `send_email(report)`: calls Email agent to send the markdown report

Finally, under `trace("Research trace")`, it runs:

- plan → search → write → (optional) email

---

## What to pay attention to (the “why”)

- **Separation of concerns**:
  - planner = “decide what to do”
  - searcher = “gather evidence”
  - writer = “synthesize”
  - emailer = “deliver”
- **Typed data between stages** (Pydantic):
  - reduces brittle string parsing
- **Concurrency**:
  - makes the workflow practical for real use
- **Tool forcing** (`tool_choice="required"`):
  - reduces hallucinated “web results”

---

## Common pitfalls (and fixes)

- **Search outputs are low quality / fluffy**:
  - tighten search agent instructions (ban filler, require bullets, require “what changed / why it matters”)
- **Planner searches are redundant**:
  - add a rule: “queries must be non-overlapping and cover different angles”
- **Long report is repetitive**:
  - require an outline with named sections + enforce “no repeated points across sections”
- **Async errors hide the root cause**:
  - temporarily run searches sequentially to isolate failures; then re-enable `gather`

---

## Daily learning routine (20–30 minutes)

- **5 min**: definitions (hosted tool, tool_choice required, structured outputs)
- **10 min**: run the pipeline with a new query and inspect:
  - planned searches
  - each search summary quality
  - writer report structure
- **10–15 min**: do one exercise below

---

## Practice exercises (pick 1 per day)

### Easy

- **Exercise A (planner quality)**: Increase `HOW_MANY_SEARCHES` from 3 → 5 and add a constraint:
  - “at least 1 query must be about risks/limitations”
  - “at least 1 query must be about market adoption”
- **Exercise B (search context size)**: change `search_context_size` from `"low"` to `"medium"` and compare summary specificity.

### Medium (recommended)

- **Exercise C (dedupe step)**: add a small function that merges/deduplicates overlapping search summaries before writing the report.
- **Exercise D (citation discipline)**: update the writer instructions to include a “Sources” section with link-style citations when possible.

### Advanced

- **Exercise E (two-pass writing)**:
  - Pass 1: writer outputs outline + claims list
  - Pass 2: writer expands into full report and checks every claim is supported by search summaries
- **Exercise F (quality guardrail)**:
  - add an evaluation agent that scores each search summary; if score < threshold, re-run that search with a refined query

---

## Quick self-check questions

- Why do we set `tool_choice="required"` for the search agent?
- What do you gain by making `PlannerAgent` output a `WebSearchPlan` object?
- Where does parallelism happen, and why?
- If the final report is wrong, which stage do you debug first: planner, searcher, or writer?


