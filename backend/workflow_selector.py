def select(user_message: str) -> str:
    """
    Keyword-based workflow selector for Microsoft Teams workflows.
    """

    msg_lower = user_message.lower()

    # -----------------------------
    # Teams Update Workflow
    # -----------------------------
    if "update" in msg_lower:
        return "TeamsUpdate"

    # -----------------------------
    # Teams Launch Workflow
    # -----------------------------
    if "teams" in msg_lower and (
        "not working" in msg_lower
        or "not launching" in msg_lower
        or "not opening" in msg_lower
        or "won't open" in msg_lower
        or "wont open" in msg_lower
        or "cannot open" in msg_lower
        or "can't open" in msg_lower
        or "cant open" in msg_lower
        or "lagging" in msg_lower
        or "slow" in msg_lower
        or "freezing" in msg_lower
        or "stuck" in msg_lower
        or "crashing" in msg_lower
    ):
        return "TeamsLaunch"

    return "Unknown"