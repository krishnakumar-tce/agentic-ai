from typing import Dict, Any
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from .constants import WEATHER_API_BASE, DATE_FORMAT

logger = logging.getLogger(__name__)

class WeatherForecastService:
    """Service for handling weather forecasts using WeatherAPI.com"""
    
    def __init__(self):
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path)
        
        self.api_key = os.getenv('WEATHERAPI_KEY')
        if not self.api_key:
            raise ValueError("Missing WEATHERAPI_KEY in .env")
    
    async def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get weather forecast for specified dates"""
        logger.info(f"Weather API - Request for: {request['city']}")
        
        async with aiohttp.ClientSession() as session:
            try:
                location = request['city']
                logger.debug(f"Querying weather for: {location}")
                
                params = {
                    'q': location,
                    'key': self.api_key,
                    'days': 14,  # Get max days
                    'aqi': 'no'
                }
                
                async with session.get(
                    WEATHER_API_BASE,
                    params=params,
                    headers={'Accept': 'application/json'}
                ) as response:
                    if not response.ok:
                        logger.error(f"Weather API error: {response.status}")
                        return {"error": f"Weather API error: {response.status}"}
                    
                    data = await response.json()
                    
                    daily_forecasts = {}
                    for forecast in data['forecast']['forecastday']:
                        date = datetime.strptime(forecast['date'], DATE_FORMAT)
                        start_date = datetime.strptime(request['start_date'], DATE_FORMAT)
                        end_date = datetime.strptime(request['end_date'], DATE_FORMAT)
                        
                        if start_date <= date <= end_date:
                            daily_forecasts[forecast['date']] = {
                                'condition': forecast['day']['condition']['text'],
                                'max_temp': round(forecast['day']['maxtemp_c']),
                                'min_temp': round(forecast['day']['mintemp_c']),
                                'rain_chance': forecast['day']['daily_chance_of_rain']
                            }
                    
                    result = {
                        'city': data['location']['name'],
                        'country': data['location']['country'],
                        'forecasts': daily_forecasts
                    }
                    
                    logger.info(f"Weather API - Retrieved {len(daily_forecasts)} days forecast")
                    return result
                    
            except Exception as e:
                logger.error(f"Error getting weather forecast: {str(e)}")
                return {"error": str(e)}