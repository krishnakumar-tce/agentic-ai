WeatherForecastSchema = {
    "type": "object",
    "required": ["city", "start_date", "end_date"],
    "properties": {
        "city": {
            "type": "string",
            "description": "City name to get weather forecast for"
        },
        "start_date": {
            "type": "string",
            "description": "Start date in YYYY-MM-DD format (must be within next 14 days)"
        },
        "end_date": {
            "type": "string",
            "description": "End date in YYYY-MM-DD format (must be within 14 days from start_date)"
        }
    },
    "additionalProperties": False
} 