# Agentic AI System

A Python-based multi-agent system for travel planning using OpenAI's GPT-4 model.

## Quick Start Guide

### Adding a New Agent with Triage Integration

1. Create your specialized agent in `config/agents.yaml`:
```yaml
agents:
  agent_your_name:  # Must start with 'agent_'
    class: BaseAgent
    name: "Your Agent Name"
    tools:
      - tool_your_inner_tool  # Your agent's specific tool
    instructions: |
      You are a specialized agent that...

      Your role is to:
      1. ...
      2. ...
      3. ...

      Guidelines:
      - ...
      - ...
```

2. Add a triage tool for your agent in `config/tools.yaml`:
```yaml
tools:
  transfer_to_agent_name:  # Must match your agent name
    class: agentic_ai.extensions.triage.tool.TriageTool
    description: Transfer to your agent for specific functionality
```

3. Update triage agent configuration in `config/agents.yaml`:
```yaml
  agent_triage:
    class: BaseAgent
    name: "Triage Agent"
    tools:
      - transfer_to_agent_trip_planner
      - transfer_to_your_name  # Add your transfer tool here
    instructions: |
      You are a triage agent that routes requests to specialized agents.
      # ... rest of instructions ...
```

### Adding a New Tool

1. Create your tool directory:
```
extensions/
└── tool_your_name/           # Must start with 'tool_' and use snake_case
    ├── __init__.py
    ├── .env                  # Tool-specific credentials
    ├── constants.py          # Tool-specific constants
    ├── schemas.py           # OpenAI function schema
    └── service.py           # Service implementation
```

2. Define your schema (schemas.py):
```python
YourNameSchema = {  # Must be {PascalCase(tool_name)}Schema
    "type": "object",
    "required": ["field1", "field2"],
    "properties": {
        "field1": {
            "type": "string",
            "description": "Description for OpenAI"
        },
        "field2": {
            "type": "integer",
            "description": "Description for OpenAI"
        }
    }
}
```

3. Implement your service (service.py):
```python
class YourNameService:  # Must be {PascalCase(tool_name)}Service
    """Service for handling your functionality"""
    
    def __init__(self):
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path)
        
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("Missing required API credentials in .env")
    
    async def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Implement your logic here
        return {"result": "..."}
```

### Key Points

1. All names are automatically inferred from the tool name
2. Required files: schemas.py, service.py, __init__.py, .env
3. Follow naming conventions exactly
4. Use .env.example files for credentials templates

## Development

1. Install dependencies:
```bash
pip install -e ".[dev]"
```

2. Set up environment files:
```bash
cp agentic_ai/.env.example agentic_ai/.env
# Update with your API keys
```

3. Run the server:
```bash
python -m agentic_ai.run
```

## API Usage

```python
import requests

response = requests.post("http://localhost:8000/chat", json={
    "messages": [
        {"role": "user", "content": "Plan a trip to Paris"}
    ],
    "conversation_id": "conv_123",
    "thread_id": "thread_456"
})

print(response.json())
```
