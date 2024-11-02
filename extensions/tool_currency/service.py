from typing import Dict, Any
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

class CurrencyService:
    """Service for currency conversion using ExchangeRate-API"""
    
    def __init__(self):
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path)
        
        self.api_key = os.getenv('EXCHANGERATE_API_KEY')
        if not self.api_key:
            raise ValueError("Missing EXCHANGERATE_API_KEY in .env")
            
        self.base_url = "https://v6.exchangerate-api.com/v6"
    
    async def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Convert amount between currencies"""
        logger.info(f"Currency API - Converting {request['amount']} {request['from_currency']} to {request['to_currency']}")
        
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{self.base_url}/{self.api_key}/pair/{request['from_currency']}/{request['to_currency']}"
                
                async with session.get(
                    url,
                    headers={'Accept': 'application/json'}
                ) as response:
                    if not response.ok:
                        logger.error(f"Currency API error: {response.status}")  # Only log status
                        return {"error": f"Currency API error: {response.status}"}
                    
                    data = await response.json()
                    
                    converted_amount = request['amount'] * data['conversion_rate']
                    logger.info(f"Currency API - Conversion completed at rate: {data['conversion_rate']}")
                    
                    return {
                        'from_amount': request['amount'],
                        'from_currency': request['from_currency'],
                        'to_amount': round(converted_amount, 2),
                        'to_currency': request['to_currency'],
                        'rate': data['conversion_rate']
                    }
                    
            except Exception as e:
                logger.error(f"Error converting currency: {str(e)}")
                raise 