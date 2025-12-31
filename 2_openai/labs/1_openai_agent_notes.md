# Daily Learning & Practice Notes — `1_openai_agent.ipynb`

This lab is the “minimum working example” of the Agents SDK:

- create an `Agent`
- run it with `Runner.run(...)`
- wrap the run in `trace(...)` so you can **see traces in the OpenAI platform**

---

## Prerequisites / setup

- **Required env var**: `OPENAI_API_KEY`
- `.env` is loaded via `load_dotenv(override=True)`
- **Tracing toggle**:
  - Tracing is enabled by default
  - If `OPENAI_AGENTS_DISABLE_TRACING=1`, tracing is disabled

---

## Definitions (memorize)

- **`Agent`**: an LLM worker with `name`, `instructions`, and a `model`.
- **`Runner.run(agent, input, ...)`**: executes a run and returns a result object.
  - `result.final_output` is the main text output.
- **`trace("workflow_name")`**: context manager that records the run for observability.
  - Trace data can be exported (if supported by the trace object).
- **Trace ID**: unique ID (useful for support / debugging).

---

## Notebook walkthrough (cell-by-cell)

### Cell 0: imports + enable tracing

What it does:

- Loads `.env`
- Checks `OPENAI_AGENTS_DISABLE_TRACING`
- Prints whether tracing is enabled

Why it matters:

- You can run agents without tracing, but traces are the easiest way to debug tool calls, latency, and errors.

### Cell 1: create an agent

Creates:

- `Agent(name="Assistant", instructions="...", model="gpt-4o-mini")`

Key idea:

- Instructions are the “policy” of the agent; model is the “engine”.

### Cell 2: run with a trace

Pattern:

- Wrap the run with `with trace("chicken_joke_trace") as t:`
- `await Runner.run(agent, "Tell a joke about a chicken")`
- Print `result.final_output`
- Print trace metadata (`t.trace_id`, `t.name`) if present
- Export trace (if `.export()` exists)

### Cell 3 (markdown): where to view traces

This is your quick checklist to confirm traces are showing up in the platform.

---

## Common pitfalls (and fixes)

- **No traces showing up**:
  - Ensure `OPENAI_AGENTS_DISABLE_TRACING` is not `1`
  - Wait a few seconds (traces can be async)
  - Confirm you’re in the correct OpenAI org/account in the dashboard
- **Auth errors**:
  - Make sure `OPENAI_API_KEY` is set and valid

---

## Daily learning routine (10–15 minutes)

- **3 min**: recite definitions (`Agent`, `Runner.run`, `trace`)
- **5 min**: run 3 prompts and check:
  - output quality
  - trace appears in platform
- **5 min**: do one exercise below

---

## Practice exercises (pick one per day)

- **Exercise A (trace naming)**: run 3 times with different trace names and verify you can find each in the dashboard.
- **Exercise B (instruction change)**: change the agent instructions to “answer in 3 bullet points” and see how output changes.
- **Exercise C (metadata habit)**: add a short prefix/suffix to trace names like `lab1_<topic>_<date>` to build a searchable trace history.

---

## Quick self-check questions

- What’s the difference between the **agent output** and the **trace**?
- What env var disables tracing?
- If your output looks wrong, what would you inspect in traces first?


