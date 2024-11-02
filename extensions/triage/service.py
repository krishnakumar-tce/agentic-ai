from .schemas import TriageResponse
import logging

logger = logging.getLogger(__name__)

class TriageService:
    """Service for handling request routing"""
    
    async def route_request(self, routing_name: str) -> TriageResponse:
        """Route the request to appropriate agent"""
        return TriageResponse(
            routing=routing_name,
            status="success"
        )  # Return Pydantic model, let tool handle conversion