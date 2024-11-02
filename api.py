from fastapi import FastAPI
from core.messages import ChatRequest, ChatResponse
from main import AgenticAIApplication
from core.initialize import initialize_application

app = FastAPI()
factory = initialize_application()
app_instance = AgenticAIApplication(factory=factory)

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat request"""
    result = await app_instance.process_request(
        messages=request.messages,
        conversation_id=request.conversation_id,
        thread_id=request.thread_id,
        session_id=request.session_id,
        user_id=request.user_id
    )
    
    return ChatResponse(**result) 