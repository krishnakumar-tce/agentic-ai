from core.base_tool import BaseTool
from core.messages import Message
from .service import TriageService
from .schemas import TriageResponse
import logging

logger = logging.getLogger(__name__)

class TriageTool(BaseTool):
    """Tool for routing requests to specialized agents"""
    
    def __init__(self, name: str, description: str):
        super().__init__(
            name=name,
            description=description,
            schema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        )
        self.service = TriageService()
    
    async def execute(self, **kwargs):
        """Execute triage routing"""
        response = await self.service.route_request(self.name)
        return response.model_dump() 