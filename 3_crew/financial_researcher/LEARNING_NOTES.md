# CrewAI Financial Researcher Project - Learning Notes

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Differences from Debate Project](#key-differences-from-debate-project)
3. [Project Structure](#project-structure)
4. [Step-by-Step Execution Flow](#step-by-step-execution-flow)
5. [Tools Integration](#tools-integration)
6. [Task Context and Data Flow](#task-context-and-data-flow)
7. [Configuration Files Explained](#configuration-files-explained)
8. [How to Run the Project](#how-to-run-the-project)
9. [Common Issues & Solutions](#common-issues--solutions)
10. [Customization Guide](#customization-guide)
11. [Key Takeaways](#key-takeaways)

---

## Project Overview

This project creates an **AI-powered financial research system** that:
1. **Researcher Agent**: Conducts web research on a company using SerperDevTool
2. **Analyst Agent**: Analyzes the research findings and creates a comprehensive report

**Example Use Case**: Research "Apple" company and generate a professional financial report

**Key Features**:
- ✅ Web search integration via SerperDevTool
- ✅ Two-stage research and analysis workflow
- ✅ Context passing between tasks
- ✅ Professional report generation
- ✅ Sequential task execution

---

## Key Differences from Debate Project

| Feature | Debate Project | Financial Researcher Project |
|---------|---------------|------------------------------|
| **Agents** | 2 agents (debater, judge) | 2 agents (researcher, analyst) |
| **Tools** | No tools | SerperDevTool for web search |
| **Tasks** | 3 tasks (propose, oppose, decide) | 2 tasks (research, analysis) |
| **Output** | 3 separate files | 1 consolidated report |
| **Context** | No context passing | Analysis task uses research context |
| **Purpose** | Argumentation | Information gathering & analysis |

---

## Project Structure

```
financial_researcher/
├── src/
│   └── financial_researcher/
│       ├── main.py              # Entry point - runs the crew
│       ├── crew.py              # Defines agents, tasks, and crew with tools
│       ├── config/
│       │   ├── agents.yaml      # Agent definitions (researcher, analyst)
│       │   └── tasks.yaml       # Task definitions (research, analysis)
│       └── tools/
│           └── custom_tool.py  # Example custom tool (not used in this project)
├── output/
│   └── report.md               # Generated financial report
├── knowledge/                  # Knowledge base (optional)
├── .env                        # API keys (OPENAI_API_KEY, SERPER_API_KEY)
├── pyproject.toml              # Project dependencies
└── README.md                   # Project documentation
```

---

## Step-by-Step Execution Flow

### Step 1: Entry Point (`main.py`)
```python
def run():
    inputs = {
        'company': 'Apple'
    }
    result = ResearchCrew().crew().kickoff(inputs=inputs)
```

**What happens:**
1. Creates output directory if it doesn't exist
2. Creates a `ResearchCrew` instance
3. Passes company name as input
4. Kicks off the crew execution
5. Prints and saves the result

### Step 2: Crew Initialization (`crew.py`)
```python
@CrewBase
class ResearchCrew():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
```

**What happens:**
1. Loads agent configurations from `agents.yaml`
2. Loads task configurations from `tasks.yaml`
3. Creates agent instances with tools
4. Creates task instances with context relationships
5. Assembles the crew

### Step 3: Agent Creation with Tools

**Researcher Agent:**
```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        verbose=True,
        tools=[SerperDevTool()]  # ⭐ Tool integration
    )
```

**Key Points:**
- Has access to `SerperDevTool` for web search
- Can search the internet for current information
- Uses OpenAI GPT-4o-mini model

**Analyst Agent:**
```python
@agent
def analyst(self) -> Agent:
    return Agent(
        config=self.agents_config['analyst'],
        verbose=True
        # No tools - focuses on analysis
    )
```

### Step 4: Task Creation with Context

**Research Task:**
```python
@task
def research_task(self) -> Task:
    return Task(
        config=self.tasks_config['research_task']
    )
```

**Analysis Task:**
```python
@task
def analysis_task(self) -> Task:
    return Task(
        config=self.tasks_config['analysis_task'],
        output_file='output/report.md'  # ⭐ Direct output file
    )
```

**Key Point**: The `analysis_task` has `context: [research_task]` in YAML, meaning it receives the research results as input.

### Step 5: Crew Assembly
```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,  # Tasks run one after another
        verbose=True,
    )
```

### Step 6: Execution Flow
```
1. Research Task → Researcher Agent → Uses SerperDevTool → Gathers information
2. Analysis Task → Analyst Agent → Uses research context → Creates report.md
```

**Process Type: Sequential**
- Research task completes first
- Analysis task receives research results as context
- Final output saved to `output/report.md`

---

## Tools Integration

### What is SerperDevTool?

**SerperDevTool** is a web search tool that allows agents to search the internet for current information.

**Location**: Part of `crewai_tools` package
```python
from crewai_tools import SerperDevTool
```

### How Tools Work

1. **Tool Availability**: Adding `tools=[SerperDevTool()]` makes the tool available to the agent
2. **Agent Decision**: The agent (LLM) decides when to use the tool based on:
   - Task requirements
   - Information needs
   - Tool description
3. **Automatic Usage**: When the agent needs current information, it will:
   - Recognize it needs to search
   - Call SerperDevTool with a search query
   - Use the results to complete the task

### Setting Up SerperDevTool

1. **Get API Key**: Sign up at https://serper.dev/
2. **Add to .env**:
   ```env
   SERPER_API_KEY=your_serper_api_key_here
   ```
3. **Install Dependency**: Already included in `crewai[tools]`

### Tool Usage Example

When the researcher agent receives:
```
"Conduct research on Apple company, including recent news"
```

The agent will:
1. Recognize it needs current information
2. Call `SerperDevTool` with query: "Apple company recent news 2024"
3. Receive search results
4. Use results to complete research task

### Tool Output Format

SerperDevTool returns:
- **Organic results**: Title, link, snippet
- **Knowledge graph**: Structured data
- **People Also Ask**: Related questions
- **News results**: Recent news articles

---

## Task Context and Data Flow

### Understanding Context

In `tasks.yaml`, the `analysis_task` has:
```yaml
analysis_task:
  context:
    - research_task
```

**What this means:**
- The `analysis_task` receives the output from `research_task` as input
- The analyst agent can see what the researcher found
- This enables the analyst to analyze the research findings

### Data Flow Diagram

```
┌─────────────────┐
│  Research Task  │
│  (Researcher)   │
│                 │
│  Uses:          │
│  - SerperDevTool│
│  - Web Search   │
└────────┬────────┘
         │
         │ Output: Research findings
         │
         ▼
┌─────────────────┐
│ Analysis Task   │
│ (Analyst)       │
│                 │
│ Receives:       │
│ - Research data │
│                 │
│ Creates:        │
│ - report.md     │
└─────────────────┘
```

### Context vs No Context

**With Context** (this project):
```yaml
analysis_task:
  context:
    - research_task  # Analyst sees research results
```

**Without Context**:
```yaml
analysis_task:
  # No context - Analyst works independently
```

**Benefits of Context:**
- Analyst can reference specific research findings
- More coherent and connected output
- Better analysis based on actual research data

---

## Configuration Files Explained

### `agents.yaml` - Agent Definitions

```yaml
researcher:
  role: >
    Senior Financial Researcher for {company}
  goal: >
    Research the company, news and potential for {company}
  backstory: >
    You're a seasoned financial researcher with a talent for finding
    the most relevant information about {company}.
  llm: openai/gpt-4o-mini
```

**Key Points:**
- `{company}` is a variable replaced with actual company name
- `role`, `goal`, `backstory` guide agent behavior
- `llm` specifies which AI model to use

### `tasks.yaml` - Task Definitions

```yaml
research_task:
  description: >
    Conduct thorough research on company {company}. Focus on:
    1. Current company status and health
    2. Historical company performance
    3. Major challenges and opportunities
    4. Recent news and events
    5. Future outlook and potential developments
  expected_output: >
    A comprehensive research document with well-organized sections
  agent: researcher

analysis_task:
  description: >
    Analyze the research findings and create a comprehensive report
  expected_output: >
    A polished, professional report
  agent: analyst
  context:
    - research_task  # ⭐ Receives research output
  output_file: output/report.md  # ⭐ Where to save
```

**Key Points:**
- `agent` assigns task to specific agent
- `context` passes data between tasks
- `output_file` specifies where to save results
- `{company}` variable is replaced with actual value

---

## How to Run the Project

### Prerequisites
1. **Python 3.10-3.13** installed
2. **UV package manager**: `pip install uv`
3. **CrewAI CLI**: `pip install crewai`
4. **API Keys** set in `.env` file

### Step 1: Install Dependencies
```bash
cd /path/to/financial_researcher
crewai install
# OR
uv sync
```

### Step 2: Set Up API Keys
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**Get API Keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **Serper**: https://serper.dev/ (free tier available)

### Step 3: Run the Crew
```bash
crewai run
```

### Step 4: Check Output
Results will be in `output/report.md`:
- Executive summary
- Company research findings
- Analysis and insights
- Market outlook

---

## Common Issues & Solutions

### Issue 1: `ModuleNotFoundError: No module named 'tools'`
**Problem**: Incorrect import statement
**Solution**: 
```python
# ❌ Wrong
from tools import SerperDevTool

# ✅ Correct
from crewai_tools import SerperDevTool
```

### Issue 2: `KeyError: 'analyst'` or `KeyError: 'researcher'`
**Problem**: Config file paths not declared
**Solution**: Add to `crew.py`:
```python
@CrewBase
class ResearchCrew():
    agents_config = 'config/agents.yaml'  # ⭐ Add this
    tasks_config = 'config/tasks.yaml'    # ⭐ Add this
```

### Issue 3: `SERPER_API_KEY is required`
**Problem**: Serper API key not set
**Solution**: 
1. Get key from https://serper.dev/
2. Add to `.env`: `SERPER_API_KEY=your_key_here`

### Issue 4: Agent not using SerperDevTool
**Problem**: Tool not being called
**Solution**:
- Ensure task description mentions needing current/recent information
- Check that `SERPER_API_KEY` is set correctly
- Verify tool is added to agent: `tools=[SerperDevTool()]`

### Issue 5: `OPENAI_API_KEY is required`
**Problem**: OpenAI API key not set
**Solution**: Add to `.env`: `OPENAI_API_KEY=your_key_here`

### Issue 6: Context not working
**Problem**: Analysis task doesn't see research results
**Solution**: Ensure `tasks.yaml` has:
```yaml
analysis_task:
  context:
    - research_task
```

---

## Customization Guide

### Change the Company
Edit `src/financial_researcher/main.py`:
```python
inputs = {
    'company': 'Microsoft',  # Change from 'Apple'
}
```

### Add More Tools
Edit `src/financial_researcher/crew.py`:
```python
from crewai_tools import SerperDevTool, BraveSearchTool

@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        verbose=True,
        tools=[
            SerperDevTool(),
            BraveSearchTool()  # Add another tool
        ]
    )
```

### Modify Research Focus
Edit `src/financial_researcher/config/tasks.yaml`:
```yaml
research_task:
  description: >
    Conduct research on {company}. Focus on:
    1. Financial performance (revenue, profit, growth)
    2. Market position and competition
    3. Product portfolio
    4. Management team
    # Add your custom research areas
```

### Change Output Format
Edit `src/financial_researcher/config/tasks.yaml`:
```yaml
analysis_task:
  expected_output: >
    A detailed report in JSON format with sections for:
    - Executive Summary
    - Financial Analysis
    - Risk Assessment
    - Recommendations
```

### Add a Third Agent
1. Add to `agents.yaml`:
```yaml
fact_checker:
  role: >
    Fact Checker for {company} research
  goal: >
    Verify the accuracy of research findings
  backstory: >
    You're an expert fact-checker with attention to detail
  llm: openai/gpt-4o-mini
```

2. Add to `crew.py`:
```python
@agent
def fact_checker(self) -> Agent:
    return Agent(
        config=self.agents_config['fact_checker'],
        verbose=True
    )
```

3. Add task in `tasks.yaml`:
```yaml
fact_check_task:
  description: >
    Verify the accuracy of research findings about {company}
  agent: fact_checker
  context:
    - research_task
```

### Customize Tool Behavior
```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        verbose=True,
        tools=[
            SerperDevTool(
                n_results=20,  # Get more results
                search_type="news"  # Search news only
            )
        ]
    )
```

---

## Key Takeaways

### 1. **Tools Enable Real-Time Information**
- Tools like SerperDevTool allow agents to access current information
- Agents decide when to use tools based on task requirements
- Tools are essential for research tasks that need up-to-date data

### 2. **Context Passing Between Tasks**
- Use `context` in `tasks.yaml` to pass data between tasks
- Enables agents to build on previous work
- Creates a coherent workflow

### 3. **Two-Stage Workflow Pattern**
- **Stage 1**: Gather information (research task)
- **Stage 2**: Process and analyze (analysis task)
- Common pattern for research projects

### 4. **Tool Integration Pattern**
```python
# 1. Import tool
from crewai_tools import SerperDevTool

# 2. Add to agent
tools=[SerperDevTool()]

# 3. Agent uses it automatically when needed
```

### 5. **Output File Management**
- Use `output_file` in task config to save results
- Creates organized output structure
- Easy to track generated content

### 6. **Variable Interpolation**
- Use `{company}` in YAML files
- Pass values via `inputs` dictionary
- Makes agents and tasks reusable

### 7. **Sequential Process Benefits**
- Ensures research completes before analysis
- Context is available when needed
- Predictable execution order

### 8. **Tool vs No Tool Agents**
- **Researcher**: Has tools (needs to search)
- **Analyst**: No tools (focuses on analysis)
- Match tools to agent roles

---

## Comparison: With vs Without Tools

### Without Tools (Debate Project)
```python
@agent
def debater(self) -> Agent:
    return Agent(
        config=self.agents_config['debater'],
        verbose=True
        # No tools - uses only LLM knowledge
    )
```
- Uses only pre-trained knowledge
- Cannot access current information
- Good for argumentation, analysis

### With Tools (This Project)
```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        verbose=True,
        tools=[SerperDevTool()]  # Can search the web
    )
```
- Can access real-time information
- Searches the internet when needed
- Good for research, fact-finding

---

## Next Steps for Learning

1. **Experiment with Different Companies**: Try various companies
2. **Add More Tools**: Integrate other tools (BraveSearch, ArxivPaper, etc.)
3. **Modify Research Scope**: Change what information to gather
4. **Add More Agents**: Create specialized agents (fact-checker, data analyst, etc.)
5. **Customize Output Format**: Change report structure and style
6. **Add Knowledge Base**: Use the `knowledge/` directory for context
7. **Experiment with Process Types**: Try hierarchical or consensual processes

---

## Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI Tools Documentation](https://github.com/joaomdmoura/crewai-tools)
- [Serper API Documentation](https://serper.dev/docs)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [CrewAI Discord](https://discord.gg/X4JWnZnxPb)

---

## Summary

This project demonstrates:
- ✅ Tool integration (SerperDevTool for web search)
- ✅ Context passing between tasks
- ✅ Two-stage research and analysis workflow
- ✅ Professional report generation
- ✅ Sequential task execution
- ✅ Real-time information gathering

The financial researcher crew shows how agents can work together with tools to gather current information and create comprehensive reports, making it perfect for research tasks that require up-to-date data.

