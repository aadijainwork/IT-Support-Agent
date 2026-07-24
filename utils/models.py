from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    workflow: str
    success: bool
    logs: List[str]

class WorkflowContext(BaseModel):
    user_message: str
    workflow: str
    logs: List[str] = Field(default_factory=list)
    success: bool = True
    data: Dict[str, Any] = Field(default_factory=dict)
