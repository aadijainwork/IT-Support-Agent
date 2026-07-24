from utils.models import ChatResponse
from workflows import teams_update

WORKFLOW_MAP = {
    "TeamsUpdate": teams_update.execute
}

def run(workflow_name: str) -> ChatResponse:
    """
    Executes the specified workflow and returns its ChatResponse.
    If the workflow is unknown, returns an unsupported issue response.
    """
    workflow_func = WORKFLOW_MAP.get(workflow_name)
    
    if workflow_func:
        return workflow_func()
        
    return ChatResponse(
        workflow="Unknown",
        success=False,
        logs=["Workflow not recognized or issue is unsupported."]
    )
