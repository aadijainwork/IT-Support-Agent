import re

WORKFLOW_KEYWORDS = {
    "TeamsUpdate": [
        "teams update",
        "update teams",
        "teams updating",
        "teams upgrade",
        "update",
        "updating",
        "updated",
        "upgrade",
        "upgrading",
        "version",
        "latest version",
        "update failed",
        "cannot update",
        "cant update",
        "won't update",
        "wont update",
        "not updating",
        "failed to update",
        "stuck updating",
        "repair"
    ],
    "TeamsLaunch": [
        "teams launch",
        "launch teams",
        "open teams",
        "start teams",
        "teams wont open",
        "teams won't open",
        "teams wont launch",
        "teams won't launch",
        "teams crashing",
        "teams crash",
        "teams freeze",
        "launch",
        "launching",
        "launched",
        "open",
        "opening",
        "opens",
        "start",
        "starting",
        "started",
        "loading",
        "crash",
        "crashing",
        "crashes",
        "crashed",
        "won't open",
        "wont open",
        "won't launch",
        "wont launch",
        "not launching",
        "not opening",
        "failed to launch",
        "failed to open",
        "cannot launch",
        "cannot open",
        "cant launch",
        "cant open",
        "freeze",
        "freezing",
        "freezes",
        "closes",
        "close",
        "closing"
    ],
    "OutlookLaunch": [
        "outlook launch",
        "launch outlook",
        "open outlook",
        "start outlook",
        "outlook wont open",
        "outlook won't open",
        "outlook wont launch",
        "outlook won't launch",
        "outlook not launching",
        "outlook not opening",
        "outlook crashing",
        "outlook crash",
        "outlook freeze",
        "outlook safe mode",
        "outlook fails to start",
        "outlook won't start",
        "launch",
        "launching",
        "launched",
        "open",
        "opening",
        "opens",
        "start",
        "starting",
        "started",
        "loading",
        "crash",
        "crashing",
        "crashes",
        "crashed",
        "won't open",
        "wont open",
        "won't launch",
        "wont launch",
        "not launching",
        "not opening",
        "failed to launch",
        "failed to open",
        "cannot launch",
        "cannot open",
        "cant launch",
        "cant open",
        "freeze",
        "freezing",
        "freezes",
        "closes",
        "close",
        "closing"
    ]
}


def _normalize_text(text: str) -> str:
    """
    Lowercases text, removes punctuation, and collapses whitespace.
    """
    text = text.lower()
    # Remove apostrophes so "isn't" becomes "isnt", "won't" becomes "wont"
    text = text.replace("'", "")
    # Replace non-alphanumeric characters with spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Collapse multiple spaces
    return " ".join(text.split())


def select(user_message: str) -> str:
    """
    Keyword scoring workflow selector for Teams and Outlook workflows.
    Calculates match score for each registered workflow and returns the best match.
    Returns 'Unknown' if all workflows score zero.
    """
    normalized_msg = _normalize_text(user_message)
    if not normalized_msg:
        return "Unknown"

    best_workflow = "Unknown"
    highest_score = 0

    for workflow, keywords in WORKFLOW_KEYWORDS.items():
        # App-context exclusion: don't match Outlook workflows if explicitly mentioning teams without outlook
        if workflow.startswith("Outlook") and "outlook" not in normalized_msg and "teams" in normalized_msg:
            continue
        if workflow.startswith("Teams") and "teams" not in normalized_msg and "outlook" in normalized_msg:
            continue

        score = 0
        for kw in keywords:
            kw_norm = _normalize_text(kw)
            if kw_norm and kw_norm in normalized_msg:
                score += len(kw_norm.split())

        # Give boost if app name matches workflow domain
        if workflow.startswith("Outlook") and "outlook" in normalized_msg:
            score += 2
        if workflow.startswith("Teams") and "teams" in normalized_msg:
            score += 2

        if score > highest_score:
            highest_score = score
            best_workflow = workflow

    return best_workflow


