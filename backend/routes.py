from fastapi import APIRouter
from utils.models import ChatRequest, ChatResponse
from backend import workflow_selector, workflow_registry

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    workflow_name = workflow_selector.select(request.message)
    context = workflow_registry.run(workflow_name, user_message=request.message)
    
    return ChatResponse(
        workflow=context.workflow,
        success=context.success,
        logs=context.logs
    )
