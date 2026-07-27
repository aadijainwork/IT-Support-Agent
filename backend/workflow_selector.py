import re

WORKFLOW_KEYWORDS = {
    "TeamsUpdate": [
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
    Keyword scoring workflow selector for Microsoft Teams and system workflows.
    Calculates match score for each registered workflow and returns the best match.
    Returns 'Unknown' if all workflows score zero.
    """
    normalized_msg = _normalize_text(user_message)
    if not normalized_msg:
        return "Unknown"

    best_workflow = "Unknown"
    highest_score = 0

    for workflow, keywords in WORKFLOW_KEYWORDS.items():
        score = 0
        for kw in keywords:
            kw_norm = _normalize_text(kw)
            if kw_norm and kw_norm in normalized_msg:
                # Assign weight based on number of words in phrase
                phrase_weight = len(kw_norm.split())
                score += phrase_weight

        if score > highest_score:
            highest_score = score
            best_workflow = workflow

    return best_workflow

