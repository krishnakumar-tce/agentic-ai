# Foursquare API Base URL
FOURSQUARE_API_BASE = "https://api.foursquare.com/v3"

# Search parameters
SEARCH_RADIUS_METERS = 5000  # 5km radius
RESULTS_LIMIT = 10  # Top 10 places

# Typical costs by category only, no specific places
TYPICAL_COSTS = {
    "arts": {
        "default": 15  # Average museum/arts venue cost
    },
    "entertainment": {
        "default": 25  # Average entertainment venue cost
    },
    "landmarks": {
        "default": 10  # Average landmark entry cost
    },
    "food": {
        "default": 30  # Average restaurant cost
    },
    "nightlife": {
        "default": 20  # Average nightlife venue cost
    },
    "outdoors": {
        "default": 0  # Most outdoor places are free
    },
    "shopping": {
        "default": 0  # No entry cost for shops
    }
}

# Category mappings to Foursquare IDs
PLACE_CATEGORIES = [
    "arts",
    "entertainment",
    "landmarks",
    "food",
    "nightlife", 
    "outdoors",
    "shopping"
]

# Foursquare category IDs
CATEGORY_IDS = {
    "arts": "10000",        # Arts & Entertainment
    "entertainment": "10035",# Entertainment venues
    "landmarks": "16000",    # Landmarks & Outdoors
    "food": "13000",        # Food
    "nightlife": "10032",   # Nightlife
    "outdoors": "16000",    # Outdoors & Recreation
    "shopping": "17000"     # Shops & Services
} 