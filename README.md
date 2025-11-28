# agents

## Setup

### Credentials Configuration

This project uses environment variables to manage API keys and credentials. Follow these steps to set up:

1. **Create a `.env` file** in the root directory of the project:
   ```bash
   touch .env
   ```

2. **Add your API keys** to the `.env` file:
   ```env
   # Required
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional (add as needed)
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   POLYGON_API_KEY=your_polygon_api_key_here
   ```

3. **The `.env` file is already in `.gitignore`** - your credentials will not be committed to version control.

### Using Credentials in Code

The project includes a `credentials.py` module for easy access to API keys:

```python
from credentials import get_openai_key, get_anthropic_key, get_env_var

# Get required credentials (raises error if not set)
openai_key = get_openai_key()
anthropic_key = get_anthropic_key()

# Get optional credentials (returns None if not set)
langsmith_key = get_langsmith_key()

# Get any environment variable
custom_key = get_env_var("CUSTOM_KEY", required=True)
```

### Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys
- **LangSmith**: https://smith.langchain.com/settings
- **SendGrid**: https://app.sendgrid.com/settings/api_keys
- **Polygon**: https://polygon.io/dashboard/api-keys