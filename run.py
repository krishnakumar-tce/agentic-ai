from core.load_env import load_environment
import uvicorn
from api import app

if __name__ == "__main__":
    # Load environment variables
    load_environment()
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 