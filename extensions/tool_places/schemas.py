from .constants import PLACE_CATEGORIES

PlacesSchema = {
    "type": "object",
    "required": ["city", "categories"],
    "properties": {
        "city": {
            "type": "string",
            "description": "City name to find places in"
        },
        "categories": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": PLACE_CATEGORIES
            },
            "description": "Categories of places to find. Must be one or more of: arts, entertainment, landmarks, food, nightlife, outdoors, shopping"
        }
    },
    "additionalProperties": False
} 