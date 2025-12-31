# Daily Learning & Practice Notes — `2_openai_agent.ipynb`

This lab builds practical “agent workflows” in steps:

- **stream** model output token-by-token
- run **multiple agents in parallel** (`asyncio.gather`)
- create **tools** from Python functions (`@function_tool`)
- convert an **Agent into a tool** (`Agent.as_tool`)
- orchestrate with a **Sales Manager** agent
- introduce **handoffs** to a specialist **Email Manager** agent

---

## Prerequisites / setup

- `.env` is loaded via `load_dotenv(override=True)`
- **Email sending** uses SendGrid:
  - Needs `SENDGRID_API_KEY`
  - The sender (`from_email`) must be verified in SendGrid
  - Be careful: these functions can send real emails

---

## Definitions (must know)

### Core

- **`Agent`**: role + instructions + model (+ optional tools/handoffs).
- **`Runner.run(agent, input)`**: runs the agent and returns a result (use `result.final_output`).
- **`trace("name")`**: records the run for debugging/observability.

### Streaming

- **`Runner.run_streamed(...)`**: returns a streaming run handle.
- **`stream_events()`**: async iterator over events coming from the model.
- **`ResponseTextDeltaEvent`**: an event type representing “text delta” chunks (partial text).
  - You print `event.data.delta` to show live output.

### Parallelism

- **`asyncio.gather(a, b, c)`**: run multiple awaits concurrently.
  - Here: generate drafts from multiple sales agents at the same time.

### Tools

- **`@function_tool`**: wraps a Python function so the agent can call it (tool calling).
  - The SDK generates a JSON schema for the tool automatically.
- **`Agent.as_tool(...)`**: converts an Agent into a tool callable by other agents.

### Handoffs vs tools (key concept)

- **Tool call**: control returns to the caller after the tool finishes.
- **Handoff**: control transfers to another agent to finish the job.

---

## Notebook walkthrough (cell-by-cell)

### Cells 0–2: imports + SendGrid test

- Imports `function_tool`, `trace`, and streaming event type
- Sends a test email and prints status code (e.g., `202` = accepted by SendGrid)

Daily takeaway: validate your “side effects” (email) before building agent orchestration.

### Cells 3–4: define 3 sales agents (same task, different styles)

You create:

- professional agent
- engaging/humorous agent
- concise agent

### Cell 5: streaming output (live printing)

Pattern:

- `result = Runner.run_streamed(sales_agent1, input="...")`
- Iterate `async for event in result.stream_events():`
- Filter for raw text delta events
- Print `event.data.delta` as it arrives

Why it matters:

- Great for UIs/CLI where you want “typing” behavior and faster perceived latency.

### Cell 6: parallel draft generation

Pattern:

- Wrap in `trace("Parallel cold emails")`
- Use `await asyncio.gather(Runner.run(...), Runner.run(...), Runner.run(...))`
- Extract `result.final_output` from each run

Why it matters:

- Draft diversity + speed. Parallel calls are typically faster than sequential.

### Cells 7–8: “sales_picker” agent to select the best draft

Pattern:

- A separate agent receives the concatenated drafts
- Instruction: “pick the best, return ONLY the chosen email”

Why it matters:

- This is the simplest form of “manager”/“judge” pattern.

### Part 2: tools (cells 10–16)

#### Cell 12: `send_email` tool via `@function_tool`

You define:

- `send_email(body: str)` that sends a plain-text email via SendGrid

Key idea:

- The decorator converts it into a tool the model can call safely via schema.

#### Cells 14–15: agent-as-tool

You define:

- `tool1 = sales_agent1.as_tool(...)` and similarly for agent2/agent3
- `tools = [tool1, tool2, tool3, send_email]`

Now a manager agent can:

- call `sales_agent*` tools to draft emails
- call `send_email` tool to send exactly one

#### Cell 16: Sales Manager agent (tool-using orchestrator)

Instructions enforce:

- use tools to generate drafts (don’t write drafts directly)
- select best
- call `send_email` exactly once
- (also: “no emojis” constraint — note the typo “Aslo” is harmless)

### Handoffs + Email Manager (cells 17–23)

- Cell 17 explains the concept difference (tool vs handoff).
- Cells 18–21 build an Email Manager:
  - `subject_writer` agent-as-tool
  - `html_converter` agent-as-tool
  - `send_html_email` function tool
  - Email Manager instructions: subject → HTML → send
  - `handoff_description` helps routing
- Cell 23 builds a Sales Manager that:
  - uses sales agent tools to generate drafts
  - selects best
  - **hands off** to Email Manager to format + send

---

## Common pitfalls (and fixes)

- **Streaming prints nothing**:
  - Ensure you’re filtering the right event type (`raw_response_event` + `ResponseTextDeltaEvent`)
- **Parallel runs fail**:
  - One failure can fail the whole `gather`; debug by running agents one-by-one first.
- **Emails not delivered**:
  - `202` means accepted, not “delivered”
  - Check SendGrid activity logs and sender verification
- **Agents don’t follow “must use tools”**:
  - Make tools clearly named and described
  - Add explicit “Crucial Rules” like the notebook does

---

## Daily learning routine (20–30 minutes)

- **5 min**: definitions (streaming, tools, handoffs)
- **10 min**: run:
  - one streamed draft
  - one parallel run (3 drafts)
  - one picker selection
- **10–15 min**: do 1 exercise below

---

## Practice exercises (do 1 per day)

### Easy

- **Exercise A (streaming filter)**: print every event type once to learn the event stream shape, then restore the filter.
- **Exercise B (style constraints)**: add “≤120 words” to each sales agent instructions and compare outputs.

### Medium (recommended)

- **Exercise C (rubric picker)**: change `sales_picker` to return a JSON-like response:
  - winner index + 3 short scores (clarity, relevance, CTA)
- **Exercise D (tool safety)**: add a “dry-run” boolean argument to `send_email` / `send_html_email`:
  - if dry-run, return the payload instead of sending

### Advanced

- **Exercise E (handoff routing)**: add a second handoff agent (e.g., “Compliance Reviewer”) and teach Sales Manager when to route.
- **Exercise F (structured outputs)**: use a Pydantic model output for the picker and/or manager (winner + reason + constraints met).

---

## Quick self-check questions

- When should you use **streaming** vs normal `Runner.run`?
- What’s the difference between **tool call** and **handoff** in control flow?
- Why is `asyncio.gather` useful for draft generation?
- Where would you enforce “don’t send real emails”: tool layer, manager instructions, or guardrail?


