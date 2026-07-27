def select(user_message: str) -> str:
    """
    Keyword-based workflow selector for Microsoft Teams and system workflows.
    """
    msg_lower = user_message.lower()
    
    if "teams" in msg_lower or "launch" in msg_lower or "update" in msg_lower:
        if any(kw in msg_lower for kw in ["launch", "open", "start", "run", "crash"]):
            return "TeamsLaunch"
        if any(kw in msg_lower for kw in ["update", "upgrade", "version", "repair"]):
            return "TeamsUpdate"
        return "TeamsLaunch"
        
    return "Unknown"
