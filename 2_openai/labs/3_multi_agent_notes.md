# Daily Learning & Practice Notes — `3_multi_agent.ipynb`

Use this note as your **daily revision + practice checklist** for the multi-agent lab.

---

## What you build in this lab (1–2 lines)

A small “Automated SDR” workflow:

- 3 **Sales agents** (different writing styles) generate drafts
- a **Sales Manager** agent selects the best draft
- the winning draft is **handed off** to an **Email Manager** agent
- the Email Manager writes a **subject**, converts the body to **HTML**, then **sends** the email
- an **input guardrail** blocks runs when a personal name is included (demo)

---

## Prerequisites / setup (must know)

- **Environment variables** (from `.env` via `load_dotenv(override=True)`):
  - **Required**: `OPENAI_API_KEY`
  - **Optional** (for this notebook’s alternate model providers):
    - `GOOGLE_API_KEY` (Gemini via OpenAI-compatible endpoint)
    - `DEEPSEEK_API_KEY`
    - `GROQ_API_KEY`
  - **If actually emailing**: `SENDGRID_API_KEY` (and SendGrid sender must be verified)
- **Safety**: the notebook’s `send_html_email()` sends a real email if keys are configured. Treat it like production code.

---

## Definitions (learn these first)

### Core “Agents SDK” concepts

- **`Agent`**: An LLM-backed worker with a name, instructions, optional tools, and optional handoffs.
  - Think: “role + policy + capabilities”.
- **`Runner.run(agent, input, ...)`**: Executes a workflow starting at `agent`.
  - The agent may call tools, hand off to other agents, and return a final answer.
- **`trace("name")`**: Wraps a run so it’s observable (timings, tool calls, errors) and can be viewed in tracing systems.

### Tools (how an agent “does things”)

- **Tool**: A callable function the model can invoke.
  - Two common forms in this notebook:
    - **`@function_tool`**: wraps a Python function into a tool the model can call.
    - **`Agent.as_tool(...)`**: converts an entire agent into a tool (so another agent can “call that agent” like a function).
- **`tool_name` / `tool_description`**: matter a lot. The model chooses tools partly based on names/descriptions.

### Handoffs (agent → agent)

- **Handoff**: Instead of the current agent finishing the job, it transfers the task to another agent.
  - In this notebook: Sales Manager → Email Manager.
- **`handoff_description`**: short routing metadata that helps the system know when to hand off.

### Models & providers

- **`AsyncOpenAI(base_url=..., api_key=...)`**: OpenAI SDK client that can point to any **OpenAI-compatible** endpoint.
- **`OpenAIChatCompletionsModel(model=..., openai_client=...)`**: “model adapter” used by the Agents SDK so an `Agent` can run on that client.
- **OpenAI-compatible endpoints** used here:
  - Gemini: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - DeepSeek: `https://api.deepseek.com/v1`
  - Groq: `https://api.groq.com/openai/v1`

### Guardrails (policy checks)

- **Input guardrail**: runs before/at the start of the workflow to validate the user input.
- **`@input_guardrail`**: decorator that registers a guardrail function.
- **`GuardrailFunctionOutput`**: return value containing:
  - `tripwire_triggered`: if `True`, the run is stopped with an exception (as you saw)
  - `output_info`: extra structured info (useful for debugging/logging/UI)
- **Tripwire**: a condition that “hard blocks” the run. Here: a personal name detected in the message.
- **`output_type` on an Agent**: makes the agent return structured output (here via a Pydantic model).

---

## Notebook walkthrough (cell-by-cell)

### Cells 0–2: imports + environment

- Imports:
  - Agents SDK pieces: `Agent`, `Runner`, `trace`, `function_tool`, `input_guardrail`, etc.
  - Providers: `AsyncOpenAI` and SendGrid client
- Loads `.env` and prints which keys exist (good sanity check).

### Cell 3: writing styles

Defines three “persona” instruction strings:

- professional/serious
- humorous/engaging
- concise/busy

Key idea: **same task, different instructions → different drafts**.

### Cells 4–6: connect to multiple providers and build 3 agents

- Sets three OpenAI-compatible base URLs.
- Creates three `AsyncOpenAI` clients (DeepSeek/Gemini/Groq).
- Wraps them in `OpenAIChatCompletionsModel(...)`.
- Creates three sales agents, each using a different provider/model.

Daily takeaway: multi-agent can also mean **multi-model** (diversity improves results).

### Cell 7: convert sales agents into tools

`sales_agent*.as_tool(...)` turns each sales agent into a callable tool:

- `sales_agent1(input=...)`
- `sales_agent2(input=...)`
- `sales_agent3(input=...)`

Now another agent can call them to generate drafts.

### Cells 8–12: build “Email Manager” agent + its tools

Tools used by Email Manager:

- `subject_writer` (agent-as-tool): writes a subject line
- `html_converter` (agent-as-tool): turns body → HTML
- `send_html_email` (function tool): sends via SendGrid

Email Manager agent:

- Has clear instructions: **subject → html → send**
- Has those tools attached
- Has `handoff_description` so other agents can route to it

### Cell 14: build “Sales Manager” that orchestrates + hands off

Sales Manager agent:

- Tools: the three sales agent tools
- Handoffs: `[emailer_agent]`
- Instructions force a 3-step plan:
  - generate 3 drafts (must use tools)
  - select the best
  - hand off exactly one to Email Manager

Run is wrapped in `trace("Automated SDR")`.

### Cell 15: alternate instruction set (no handoff)

This cell shows a variation: Sales Manager is told to send the email directly (but the code doesn’t actually provide a `send_email` tool here).

Daily takeaway: **instructions must match available tools** (otherwise the agent can’t comply).

### Cells 17–20: guardrails demo (blocking personal names)

1. Define `NameCheckOutput` (Pydantic schema).
2. `guardrail_agent` produces structured output: `{is_name_in_message, name}`.
3. `guardrail_against_name(...)` runs before the workflow:
   - if a personal name appears, it sets `tripwire_triggered=True`
4. `careful_sales_manager` includes `input_guardrails=[guardrail_against_name]`.
5. Running with “from Alice” triggers an exception (expected).
6. Running with “from Head of Business Development” passes.

Daily takeaway: guardrails are your “policy gate” before any expensive or risky behavior (like sending emails).

---

## Common pitfalls (and quick fixes)

- **Missing API keys**: provider tools silently fail later; always validate early (like cell 2 does).
- **SendGrid errors**:
  - missing `SENDGRID_API_KEY`
  - unverified sender email (`from_email`) in SendGrid
  - sending to wrong recipient
- **Mismatch between instructions and tools**:
  - if you say “use `send_email`” but tool is `send_html_email`, the agent will struggle.
- **Guardrail too aggressive**:
  - your guardrail can block benign input; tune it or add “allowed names/roles” logic.
- **No evaluation criteria**:
  - “pick the best draft” is vague; add a rubric (clarity, relevance, CTA, length).

---

## Daily learning routine (20–30 minutes)

- **5 min**: recite definitions
  - Agent vs tool vs handoff vs guardrail
- **10 min**: run the workflow with 2–3 different prompts
  - vary audience (“CEO”, “CTO”, “Compliance lead”)
  - vary constraints (“≤120 words”, “no jargon”, “include 1 CTA question”)
- **10–15 min**: do one exercise from the list below and commit your changes

---

## Practice exercises (do 1 per day)

### Easy (warm-up)

- **Exercise A (tool naming)**: Rename tools/descriptions to be more explicit (e.g. “draft_serious_email”, “draft_funny_email”) and observe tool choice stability.
- **Exercise B (prompt constraints)**: Add a constraint to Sales Manager instructions: “final email must be ≤ 120 words” and test.

### Medium (recommended)

- **Exercise C (add a scoring rubric tool)**:
  - Create a `@function_tool` called `score_email(body: str) -> dict` that scores clarity/relevance/CTA from 1–5.
  - Update Sales Manager instructions to score each draft and pick the highest score.
- **Exercise D (output structure)**:
  - Make Sales Manager return structured output (Pydantic): `{drafts: [...], winner: ..., reason: ...}`.

### Advanced

- **Exercise E (output guardrail)**:
  - Add an **output guardrail** that rejects emails containing emojis or containing personal names.
- **Exercise F (safe send mode)**:
  - Add a “dry run” flag so `send_html_email` doesn’t actually send unless explicitly enabled.

---

## Quick self-check questions

- Can you explain the difference between **tool call** vs **handoff**?
- Why do we wrap the provider clients with `OpenAIChatCompletionsModel`?
- What does the guardrail “tripwire” do operationally?
- If you wanted to stop the agent from emailing real people, where would you enforce it: tool layer, agent instructions, or guardrail—and why?


