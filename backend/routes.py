from fastapi import APIRouter
from utils.models import ChatRequest, ChatResponse
from backend import workflow_selector, workflow_registry

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    workflow_name = workflow_selector.select(request.message)
    return workflow_registry.run(workflow_name)
