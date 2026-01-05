# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI agents learning repository focused on exploring various AI agent frameworks and implementations. The project is organized as a series of numbered modules covering different agent technologies and approaches.

## Development Commands

### Package Management
```bash
# Install dependencies using uv (preferred)
uv pip install -r requirements.txt

# Or install from pyproject.toml
uv pip install -e .

# Activate virtual environment
source .venv/bin/activate
```

### Running Code
```bash
# Run Python files
python <path/to/file.py>

# Start Jupyter notebooks
jupyter notebook

# Run specific labs notebooks
jupyter notebook 1_foundations/labs/1_labs.ipynb
```

### Code Quality
```bash
# Run linter (ruff is installed)
ruff check .

# Format code with ruff
ruff format .
```

## Project Structure

The repository is organized into numbered modules representing progressive learning topics:

- **1_foundations/**: Core agent concepts and personal profile chatbot
  - `personalProfile/`: A chatbot system with OpenAI function calling, includes tools, personal data management, and Pushover notifications
  - `labs/`: Jupyter notebooks for experimentation
  - `me/`: Personal configuration and data

- **2_openai/**: OpenAI-specific agent implementations
  - `labs/`: Advanced notebooks including multi-agent systems and deep research
  - `deep_search/`: Deep search implementations
  - `asyncio.py`: Asynchronous OpenAI operations

## Key Architecture Patterns

### Environment Variables
The project uses `.env` files for API key management. Required keys include:
- `OPENAI_API_KEY`: Required for OpenAI operations
- `ANTHROPIC_API_KEY`: Optional for Anthropic models
- `LANGSMITH_API_KEY`: Optional for LangSmith tracing
- `PUSHOVER_USER` and `PUSHOVER_TOKEN`: For notification services

Environment variables are loaded using `python-dotenv` with fallback paths to handle different working directories.

### Agent Architecture
The personal chatbot system (`1_foundations/personalProfile/`) demonstrates:
- Function calling with OpenAI models
- Tool integration pattern with a centralized tools module
- System prompt customization based on personal data
- Gradio UI integration for interactive interfaces

### Dependencies
The project uses modern AI/ML libraries including:
- Multiple agent frameworks: `autogen`, `langgraph`, `semantic-kernel`
- LLM providers: `openai`, `anthropic`, `langchain`
- Web frameworks: `gradio` for UIs
- Utilities: `playwright` for web automation, `sendgrid` for emails

## Development Practices

### Working with Notebooks
- Notebooks in `labs/` directories are for experimentation and learning
- Each numbered notebook represents a different concept or technique
- Notebooks may have accompanying markdown notes (e.g., `4_deep_research_notes.md`)

### Module Organization
- Each numbered directory is self-contained with its own focus area
- Code is modular with clear separation between tools, data, and main logic
- The chatbot pattern in `personalProfile/` can be extended for other agents