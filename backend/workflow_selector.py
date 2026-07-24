def select(user_message: str) -> str:
    """
    Simple keyword-based mock workflow selector.
    """
    msg_lower = user_message.lower()
    
    if "teams" in msg_lower and "update" in msg_lower:
        return "TeamsUpdate"
    elif "teams" in msg_lower:
        return "TeamsUpdate"
    elif "update" in msg_lower:
        return "TeamsUpdate"
        
    return "Unknown"
