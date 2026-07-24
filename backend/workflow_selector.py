def select(user_message: str) -> str:
    """
    Keyword-based workflow selector for Microsoft Teams and system workflows.
    """
    msg_lower = user_message.lower()
    
    if "teams" in msg_lower or "update" in msg_lower:
        return "TeamsUpdate"
        
    return "Unknown"
