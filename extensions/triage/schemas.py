from pydantic import BaseModel

class TriageResponse(BaseModel):
    routing: str
    status: str = "success"

# No schema needed for triage tools as they don't take parameters 