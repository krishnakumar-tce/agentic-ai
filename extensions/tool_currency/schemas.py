from .constants import SUPPORTED_CURRENCIES

CurrencySchema = {
    "type": "object",
    "required": ["amount", "from_currency", "to_currency"],
    "properties": {
        "amount": {
            "type": "number",
            "description": "Amount to convert"
        },
        "from_currency": {
            "type": "string",
            "enum": SUPPORTED_CURRENCIES,
            "description": "Source currency code (e.g., USD, EUR, GBP)"
        },
        "to_currency": {
            "type": "string",
            "enum": SUPPORTED_CURRENCIES,
            "description": "Target currency code (e.g., USD, EUR, GBP)"
        }
    },
    "additionalProperties": False
} 