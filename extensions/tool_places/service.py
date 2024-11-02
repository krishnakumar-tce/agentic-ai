from typing import Dict, Any
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from .constants import (
    FOURSQUARE_API_BASE,
    SEARCH_RADIUS_METERS,
    RESULTS_LIMIT,
    CATEGORY_IDS,
    TYPICAL_COSTS
)
import json

logger = logging.getLogger(__name__)

class PlacesService:
    """Service for finding places using Foursquare Places API"""
    
    def __init__(self):
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path)
        
        self.api_key = os.getenv('FOURSQUARE_API_KEY')
        if not self.api_key:
            raise ValueError("Missing FOURSQUARE_API_KEY in .env")
    
    async def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Find places of interest in the specified city"""
        logger.info(f"Places API - Request for: {request['city']}")
        
        async with aiohttp.ClientSession() as session:
            try:
                all_places = []
                for category in request['categories']:
                    if category not in CATEGORY_IDS:
                        continue
                        
                    category_id = CATEGORY_IDS[category]
                    logger.debug(f"Searching places for category: {category}")
                    
                    # Query parameters according to Foursquare docs
                    params = {
                        'query': '',  # Empty query to get all places
                        'near': request['city'],  # Use city from request
                        'categories': category_id,
                        'sort': 'RATING',
                        'limit': RESULTS_LIMIT,
                        'fields': 'fsq_id,name,categories,rating,location,distance'
                    }
                    
                    async with session.get(
                        f"{FOURSQUARE_API_BASE}/places/search",
                        params=params,
                        headers={
                            'Authorization': self.api_key,
                            'Accept': 'application/json'
                        }
                    ) as response:
                        if not response.ok:
                            logger.error(f"Error from Foursquare: {response.status}")
                            continue
                            
                        places_data = await response.json()
                        
                        for place in places_data.get('results', []):
                            # Get typical cost for this place
                            cost = TYPICAL_COSTS.get(category, {}).get(
                                place['name'],  # Try exact place name
                                TYPICAL_COSTS.get(category, {}).get('default', 0)  # Or use default for category
                            )
                            
                            all_places.append({
                                'name': place['name'],
                                'category': category,
                                'rating': place.get('rating', 'Not rated'),
                                'address': place['location'].get('formatted_address', 'Address not available'),
                                'distance': f"{place.get('distance', 0)}m from city center",
                                'cost_eur': cost  # Add typical cost in EUR
                            })
                
                result = {
                    'city': request['city'],
                    'places': all_places
                }
                logger.info(f"Places API - Found {len(all_places)} places")
                return result
                
            except Exception as e:
                logger.error(f"Error finding places: {str(e)}")
                return {"error": str(e)}