from utils.models import WorkflowContext
from workflows import teams_update

WORKFLOW_MAP = {
    "TeamsUpdate": teams_update.execute
}

def run(workflow_name: str, user_message: str) -> WorkflowContext:
    """
    Executes the designated workflow module with WorkflowContext.
    """
    context = WorkflowContext(
        user_message=user_message,
        workflow=workflow_name,
        logs=[],
        success=True
    )
    
    workflow_func = WORKFLOW_MAP.get(workflow_name)
    if workflow_func:
        return workflow_func(context)
        
    context.workflow = "Unknown"
    context.success = False
    context.logs.append("Workflow not recognized or issue is unsupported.")
    return context
