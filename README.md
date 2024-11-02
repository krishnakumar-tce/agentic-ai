# Agentic AI System

A Python-based multi-agent system for travel planning using OpenAI's GPT-4o-mini model.
Included an example to show a trip planning assistant with two agents and three tools.

## Quick Start Guide

- Agents and Tools are configured completely through YAML definitions without any code.
- Write code only to implement your tool's functionality using a single "execute" method inside service.py within your tool's folder.
- There is no need to subclass the Agent or Tool base classes.
- Agents and Tools are loaded dynamically at runtime into the registry from the YAMLs and made available to the application.
- See example to follow along and implement your own agents and tools.

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
        {"role": "user", "content": "I'm planning to visit Paris, France from November 10-13, 2024. I'm interested in museums and food, and I'm coming from the US with USD. Can you help me plan my trip?"}
    ],
    "conversation_id": "conv_123",
    "thread_id": "thread_456"
})

print(response.json())
```

Response example:

```json
{
    "result": "Here's a detailed plan for your trip to Paris from November 10-13, 2024!\n\n### Weather Forecast\n- **November 10, 2024:** Partly Cloudy; Max: 16°C, Min: 12°C\n- **November 11, 2024:** Partly Cloudy; Max: 15°C, Min: 11°C\n- **November 12, 2024:** Sunny; Max: 13°C, Min: 8°C\n- **November 13, 2024:** Sunny; Max: 13°C, Min: 6°C\n\n### Attractions\n**Museums:**\n1. **Orsay Museum (Musée d'Orsay)**\n   - **Rating:** 9.5\n   - **Address:** 1 rue de la Légion d'Honneur (Quai Anatole France), 75007 Paris\n   - **Distance from city center:** 1794m\n   - **Entry Fee:** €15\n\n2. **Louvre Museum (Musée du Louvre)**\n   - **Rating:** 9.4\n   - **Address:** 99 rue de Rivoli (Place du Carrousel), 75001 Paris\n   - **Distance from city center:** 1224m\n   - **Entry Fee:** €15\n\n3. **Palais Garnier (Opéra Garnier)**\n   - **Rating:** 9.4\n   - **Address:** 8 rue Scribe (Rue Auber), 75009 Paris\n   - **Distance from city center:** 2426m\n   - **Entry Fee:** €15\n\n4. **Grand Palais**\n   - **Rating:** 9.4\n   - **Address:** 3 avenue du Général Eisenhower, 75008 Paris\n   - **Distance from city center:** 2998m\n   - **Entry Fee:** €15\n\n**Food Options:**\n1. **Hôtel de Crillon, A Rosewood Hotel**\n   - **Rating:** 9.5\n   - **Address:** 10 place de la Concorde, 75008 Paris\n   - **Distance from city center:** 2545m\n   - **Price Range:** €30\n\n2. **Dinand par Ferdi**\n   - **Rating:** 9.2\n   - **Address:** 18 rue du Boccador, 75008 Paris\n   - **Distance from city center:** 3716m\n   - **Price Range:** €30\n\n3. **Matsuhisa Paris**\n   - **Rating:** 9.1\n   - **Address:** 35-37 avenue Hoche, 75008 Paris\n   - **Distance from city center:** 4294m\n   - **Price Range:** €30\n\n4. **La Suite Girafe**\n   - **Rating:** 9.1\n   - **Address:** 1 place du Trocadéro et du Onze Novembre, 75016 Paris\n   - **Distance from city center:** 4506m\n   - **Price Range:** €30\n\n### Currency Conversion\n- **100 USD** converts to approximately **92.19 EUR** (Exchange rate: 0.9219).\n\n### Summary\nWith a mix of culture and culinary delights, your trip is set to be both enjoyable and memorable! Be sure to check opening hours for museums and make reservations for restaurants if required. Let me know if you need assistance with anything else, such as lodging or transportation!",
    "conversation_id": "conv_123",
    "thread_id": "thread_456",
    "session_id": "session_789",
    "thread_status": "complete",
    "messages": [
        {
            "role": "user",
            "content": "I'm planning to visit Paris, France from November 10-13, 2024. I'm interested in museums and food, and I'm coming from the US with USD. Can you help me plan my trip?",
            "name": null,
            "tool_calls": null,
            "tool_call_id": null
        },
        {
            "role": "assistant",
            "content": null,
            "name": null,
            "tool_calls": [
                {
                    "id": "call_ib8dHZid8T0GAJc4r4Mx6ZyX",
                    "type": "function",
                    "function": {
                        "name": "tool_weather_forecast",
                        "arguments": "{\"city\":\"Paris\",\"start_date\":\"2024-11-10\",\"end_date\":\"2024-11-13\"}"
                    }
                }
            ],
            "tool_call_id": null
        },
        {
            "role": "tool",
            "content": "{\"city\": \"Paris\", \"country\": \"France\", \"forecasts\": {\"2024-11-10\": {\"condition\": \"Partly Cloudy \", \"max_temp\": 16, \"min_temp\": 12, \"rain_chance\": 0}, \"2024-11-11\": {\"condition\": \"Partly Cloudy \", \"max_temp\": 15, \"min_temp\": 11, \"rain_chance\": 0}, \"2024-11-12\": {\"condition\": \"Sunny\", \"max_temp\": 13, \"min_temp\": 8, \"rain_chance\": 0}, \"2024-11-13\": {\"condition\": \"Sunny\", \"max_temp\": 13, \"min_temp\": 6, \"rain_chance\": 0}}}",
            "name": "tool_weather_forecast",
            "tool_calls": null,
            "tool_call_id": "call_ib8dHZid8T0GAJc4r4Mx6ZyX"
        },
        {
            "role": "assistant",
            "content": null,
            "name": null,
            "tool_calls": [
                {
                    "id": "call_E1YYwr61od0xSYlqGCng7Sn5",
                    "type": "function",
                    "function": {
                        "name": "tool_places",
                        "arguments": "{\"city\": \"Paris\", \"categories\": [\"arts\", \"food\"]}"
                    }
                },
                {
                    "id": "call_j9iO4TPwi9WUgnS9rPatkLjQ",
                    "type": "function",
                    "function": {
                        "name": "tool_currency",
                        "arguments": "{\"amount\": 100, \"from_currency\": \"USD\", \"to_currency\": \"EUR\"}"
                    }
                }
            ],
            "tool_call_id": null
        },
        {
            "role": "tool",
            "content":"{\"city\": \"Paris\", \"places\": [{\"name\": \"Orsay Museum (Mus\ée d'Orsay)\", \"category\": \"arts\", \"rating\": 9.5, \"address\": \"1 rue de la L\égion d'Honneur (Quai Anatole France), 75007 Paris\", \"distance\": \"1794m from city center\", \"cost_eur\": 15}, {\"name\": \"Max Linder Panorama\", \"category\": \"arts\", \"rating\": 9.4, \"address\": \"24 boulevard Poissonniere, 9th, 75009 Paris\", \"distance\": \"2018m from city center\", \"cost_eur\": 15}, {\"name\": \"Palais Garnier (Op\éra Garnier)\", \"category\": \"arts\", \"rating\": 9.4, \"address\": \"8 rue Scribe (Rue Auber), 75009 Paris\", \"distance\": \"2426m from city center\", \"cost_eur\": 15}, {\"name\": \"Louvre Museum (Mus\ée du Louvre)\", \"category\": \"arts\", \"rating\": 9.4, \"address\": \"99 rue de Rivoli (Place du Carrousel), 75001 Paris\", \"distance\": \"1224m from city center\", \"cost_eur\": 15}, {\"name\": \"Grand Palais\", \"category\": \"arts\", \"rating\": 9.4, \"address\": \"3 avenue du G\én\éral Eisenhower, 8e (Avenue Winston Churchill), 75008 Paris\", \"distance\": \"2998m from city center\", \"cost_eur\": 15}, {\"name\": \"Venus of Milo (V\énus de Milo)\", \"category\": \"arts\", \"rating\": 9.4, \"address\": \"Mus\ée du Louvre (Aile Sully, niveau 0, salle 345), 75001 Paris\", \"distance\": \"1109m from city center\", \"cost_eur\": 15}, {\"name\": \"La Seine Musicale\", \"category\": \"arts\", \"rating\": 9.4, \"address\": \"65 Pont Renault (\Île Seguin), 92100 Boulogne-Billancourt\", \"distance\": \"9173m from city center\", \"cost_eur\": 15}, {\"name\": \"Palais de Tokyo\", \"category\": \"arts\", \"rating\": 9.3, \"address\": \"13 avenue du Pr\ésident Wilson, 75116 Paris\", \"distance\": \"3993m from city center\", \"cost_eur\": 15}, {\"name\": \"Stade Roland Garros\", \"category\": \"arts\", \"rating\": 9.3, \"address\": \"2 bis, avenue Gordon Bennett (Boulevard d'Auteuil), 75016 Paris\", \"distance\": \"7390m from city center\", \"cost_eur\": 15}, {\"name\": \"L'Olympia\", \"category\": \"arts\", \"rating\": 9.3, \"address\": \"28 boulevard des Capucines, 9e, 75009 Paris\", \"distance\": \"2392m from city center\", \"cost_eur\": 15}, {\"name\": \"H\ôtel de Crillon, A Rosewood Hotel\", \"category\": \"food\", \"rating\": 9.5, \"address\": \"10 place de la Concorde, 75008 Paris\", \"distance\": \"2545m from city center\", \"cost_eur\": 30}, {\"name\": \"Dinand par Ferdi\", \"category\": \"food\", \"rating\": 9.2, \"address\": \"18 rue du Boccador, 75008 Paris\", \"distance\": \"3716m from city center\", \"cost_eur\": 30}, {\"name\": \"Le Jardin du Petit Palais (Petit Palais)\", \"category\": \"food\", \"rating\": 9.2, \"address\": \"avenue Winston Churchill (Avenue Winston Churchill), 75008 Paris\", \"distance\": \"2874m from city center\", \"cost_eur\": 30}, {\"name\": \"Partisan Cafe Artisanal\", \"category\": \"food\", \"rating\": 9.2, \"address\": \"36 rue de Turbigo, 75003 Paris\", \"distance\": \"1298m from city center\", \"cost_eur\": 30}, {\"name\": \"Matsuhisa Paris\", \"category\": \"food\", \"rating\": 9.1, \"address\": \"35-37 avenue Hoche, 75008 Paris\", \"distance\": \"4294m from city center\", \"cost_eur\": 30}, {\"name\": \"Jean Imbert au Plaza Ath\én\ée\", \"category\": \"food\", \"rating\": 9.1, \"address\": \"25 avenue Montaigne, 75008 Paris\", \"distance\": \"3548m from city center\", \"cost_eur\": 30}, {\"name\": \"Azur Cafe\", \"category\": \"food\", \"rating\": 9.1, \"address\": \"63 rue de Ponthieu, 75008 Paris\", \"distance\": \"3863m from city center\", \"cost_eur\": 30}, {\"name\": \"La Suite Girafe\", \"category\": \"food\", \"rating\": 9.1, \"address\": \"1 place du Trocad\éro et du Onze Novembre, 75016 Paris\", \"distance\": \"4506m from city center\", \"cost_eur\": 30}, {\"name\": \"Carette\", \"category\": \"food\", \"rating\": 9.0, \"address\": \"4 place Trocadero et du Onze Novembre 25 place des Vosges (Avenue Kl\éber), 75116 Paris\", \"distance\": \"4642m from city center\", \"cost_eur\": 30}, {\"name\": \"The Cambridge Public House\", \"category\": \"food\", \"rating\": 9.0, \"address\": \"8 rue de Poitou, 75003 Paris\", \"distance\": \"1435m from city center\", \"cost_eur\": 30}]}",
            "name": "tool_places",
            "tool_calls": null,
            "tool_call_id": "call_E1YYwr61od0xSYlqGCng7Sn5"
        },
        {
            "role": "tool",
            "content": "{\"from_amount\": 100, \"from_currency\": \"USD\", \"to_amount\": 92.19, \"to_currency\": \"EUR\", \"rate\": 0.9219}",
            "name": "tool_currency",
            "tool_calls": null,
            "tool_call_id": "call_j9iO4TPwi9WUgnS9rPatkLjQ"
        },
        {
            "role": "assistant",
            "content": "Here's a detailed plan for your trip to Paris from November 10-13, 2024!\n\n### Weather Forecast\n- **November 10, 2024:** Partly Cloudy; Max: 16°C, Min: 12°C\n- **November 11, 2024:** Partly Cloudy; Max: 15°C, Min: 11°C\n- **November 12, 2024:** Sunny; Max: 13°C, Min: 8°C\n- **November 13, 2024:** Sunny; Max: 13°C, Min: 6°C\n\n### Attractions\n**Museums:**\n1. **Orsay Museum (Musée d'Orsay)**\n   - **Rating:** 9.5\n   - **Address:** 1 rue de la Légion d'Honneur (Quai Anatole France), 75007 Paris\n   - **Distance from city center:** 1794m\n   - **Entry Fee:** €15\n\n2. **Louvre Museum (Musée du Louvre)**\n   - **Rating:** 9.4\n   - **Address:** 99 rue de Rivoli (Place du Carrousel), 75001 Paris\n   - **Distance from city center:** 1224m\n   - **Entry Fee:** €15\n\n3. **Palais Garnier (Opéra Garnier)**\n   - **Rating:** 9.4\n   - **Address:** 8 rue Scribe (Rue Auber), 75009 Paris\n   - **Distance from city center:** 2426m\n   - **Entry Fee:** €15\n\n4. **Grand Palais**\n   - **Rating:** 9.4\n   - **Address:** 3 avenue du Général Eisenhower, 75008 Paris\n   - **Distance from city center:** 2998m\n   - **Entry Fee:** €15\n\n**Food Options:**\n1. **Hôtel de Crillon, A Rosewood Hotel**\n   - **Rating:** 9.5\n   - **Address:** 10 place de la Concorde, 75008 Paris\n   - **Distance from city center:** 2545m\n   - **Price Range:** €30\n\n2. **Dinand par Ferdi**\n   - **Rating:** 9.2\n   - **Address:** 18 rue du Boccador, 75008 Paris\n   - **Distance from city center:** 3716m\n   - **Price Range:** €30\n\n3. **Matsuhisa Paris**\n   - **Rating:** 9.1\n   - **Address:** 35-37 avenue Hoche, 75008 Paris\n   - **Distance from city center:** 4294m\n   - **Price Range:** €30\n\n4. **La Suite Girafe**\n   - **Rating:** 9.1\n   - **Address:** 1 place du Trocadéro et du Onze Novembre, 75016 Paris\n   - **Distance from city center:** 4506m\n   - **Price Range:** €30\n\n### Currency Conversion\n- **100 USD** converts to approximately **92.19 EUR** (Exchange rate: 0.9219).\n\n### Summary\nWith a mix of culture and culinary delights, your trip is set to be both enjoyable and memorable! Be sure to check opening hours for museums and make reservations for restaurants if required. Let me know if you need assistance with anything else, such as lodging or transportation!",
            "name": null,
            "tool_calls": null,
            "tool_call_id": null
        }
    ],
    "error_details": null
}
```
