import re

# ============================================================
# APPLICATION DETECTION
# ============================================================

APPLICATION_KEYWORDS = {
    "Teams": [
        "teams",
        "microsoft teams",
        "ms teams",
        "teams app"
    ],

    "Outlook": [
        "outlook",
        "microsoft outlook",
        "mail",
        "email",
        "office outlook"
    ]
}


# ============================================================
# ISSUE DETECTION
# ============================================================

ISSUE_KEYWORDS = {

    "Launch": [

        # Strong phrases
        "not working",
        "is not working",
        "does not work",
        "doesnt work",
        "isnt working",

        "not opening",
        "not launching",
        "cannot open",
        "cannot launch",
        "cant open",
        "cant launch",

        "failed to open",
        "failed to launch",

        "wont open",
        "wont launch",
        "won't open",
        "won't launch",

        "will not open",
        "will not launch",

        "fails to start",
        "failed to start",

        "not responding",
        "stopped working",

        "crash",
        "crashes",
        "crashing",
        "crashed",

        "freeze",
        "freezes",
        "freezing",

        "loading forever",
        "stuck loading",

        "safe mode"
    ],


    "Restarting": [

        "keeps restarting",
        "restart loop",

        "restarting automatically",
        "automatically restarts",

        "auto restart",
        "auto restarting",

        "continuously restarting",
        "continuous restart",

        "keeps rebooting",
        "keeps reopening",

        "opens then closes",
        "opens and closes",

        "closes and reopens",

        "launches then closes",

        "opens then restarts",

        "restarting",
        "restarts"
    ],


    "Update": [

        "update failed",

        "cannot update",
        "cant update",

        "wont update",
        "won't update",

        "not updating",

        "failed to update",

        "stuck updating",

        "latest version",

        "upgrade",

        "upgrading",

        "version",

        "repair"
    ]
}


# ============================================================
# WORKFLOW MAP
# ============================================================

WORKFLOW_MAP = {

    ("Teams", "Launch"):
        "TeamsLaunch",

    ("Teams", "Restarting"):
        "TeamsRestarting",

    ("Teams", "Update"):
        "TeamsUpdate",

    ("Outlook", "Launch"):
        "OutlookLaunch",

    ("Outlook", "Restarting"):
        "OutlookRestarting"

}


# ============================================================
# NORMALIZATION
# ============================================================

def _normalize_text(text: str) -> str:

    text = text.lower()

    text = text.replace("'", "")

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    return " ".join(text.split())


# ============================================================
# LONGEST PHRASE FIRST
# ============================================================

def _sort_keywords(keywords):

    """
    Longer phrases receive priority.

    Example:

    'outlook not working'
    should beat

    'working'
    """

    return sorted(
        keywords,
        key=lambda x: len(x.split()),
        reverse=True
    )


# ============================================================
# APPLICATION DETECTION
# ============================================================

def detect_application(message):

    for app, keywords in APPLICATION_KEYWORDS.items():

        for keyword in keywords:

            if _normalize_text(keyword) in message:

                return app

    return None


# ============================================================
# ISSUE DETECTION
# ============================================================

def detect_issue(message):

    best_issue = None

    highest_score = 0

    for issue, keywords in ISSUE_KEYWORDS.items():

        score = 0

        for keyword in _sort_keywords(keywords):

            keyword = _normalize_text(keyword)

            if keyword in message:

                score += len(keyword.split()) * 3

        if score > highest_score:

            highest_score = score

            best_issue = issue

    return best_issue


# ============================================================
# PHRASE SCORING
# ============================================================

def calculate_issue_score(message: str, issue: str) -> int:
    """
    Calculates how strongly a message matches an issue type.
    Longer phrases receive higher priority than shorter phrases.
    """

    score = 0

    keywords = _sort_keywords(
        ISSUE_KEYWORDS[issue]
    )

    for keyword in keywords:

        keyword = _normalize_text(keyword)

        if keyword in message:

            words = len(keyword.split())

            # Longer phrases are much stronger
            score += words * 5

            # Exact sentence gets a large boost
            if message == keyword:
                score += 25

            # Starts with keyword
            elif message.startswith(keyword):
                score += 10

            # Ends with keyword
            elif message.endswith(keyword):
                score += 8

    return score


# ============================================================
# APPLICATION SCORE
# ============================================================

def calculate_application_score(message: str, application: str) -> int:
    """
    Confidence score for the detected application.
    """

    score = 0

    for keyword in APPLICATION_KEYWORDS[application]:

        keyword = _normalize_text(keyword)

        if keyword in message:

            score += 20

            if message.startswith(keyword):
                score += 5

    return score


# ============================================================
# EXTRA BOOST RULES
# ============================================================

def apply_bonus_rules(
    message: str,
    application: str,
    issue: str,
    score: int,
) -> int:

    # --------------------------------------------------------
    # OUTLOOK LAUNCH
    # --------------------------------------------------------

    if application == "Outlook" and issue == "Launch":

        bonus = [

            "outlook not working",
            "outlook is not working",
            "outlook isnt working",
            "outlook does not work",
            "outlook doesnt work",

            "outlook not opening",
            "outlook not launching",

            "outlook wont open",
            "outlook won't open",

            "outlook wont launch",
            "outlook won't launch",

            "cannot open outlook",
            "cannot launch outlook",

            "outlook crashed",
            "outlook crashing",

            "outlook freeze",
            "outlook frozen",

            "outlook not responding",

            "unable to open outlook",

            "outlook failed to start"

        ]

        for phrase in bonus:

            if _normalize_text(phrase) in message:

                score += 50


    # --------------------------------------------------------
    # OUTLOOK RESTART
    # --------------------------------------------------------

    if application == "Outlook" and issue == "Restarting":

        bonus = [

            "outlook keeps restarting",

            "outlook restart loop",

            "outlook keeps reopening",

            "outlook automatically restarts",

            "outlook opens then closes",

            "outlook closes and reopens"

        ]

        for phrase in bonus:

            if _normalize_text(phrase) in message:

                score += 50


    # --------------------------------------------------------
    # TEAMS LAUNCH
    # --------------------------------------------------------

    if application == "Teams" and issue == "Launch":

        bonus = [

            "teams not working",

            "teams is not working",

            "teams isnt working",

            "teams does not work",

            "teams doesnt work",

            "teams not opening",

            "teams not launching",

            "teams wont open",

            "teams won't open",

            "teams crashed",

            "teams crashing",

            "teams freeze",

            "teams frozen",

            "teams not responding"

        ]

        for phrase in bonus:

            if _normalize_text(phrase) in message:

                score += 50


    # --------------------------------------------------------
    # TEAMS RESTART
    # --------------------------------------------------------

    if application == "Teams" and issue == "Restarting":

        bonus = [

            "teams keeps restarting",

            "teams restart loop",

            "teams keeps reopening",

            "teams automatically restarts",

            "teams opens then closes",

            "teams closes and reopens"

        ]

        for phrase in bonus:

            if _normalize_text(phrase) in message:

                score += 50


    # --------------------------------------------------------
    # TEAMS UPDATE
    # --------------------------------------------------------

    if application == "Teams" and issue == "Update":

        bonus = [

            "teams update failed",

            "teams not updating",

            "cannot update teams",

            "cant update teams",

            "teams latest version",

            "teams stuck updating",

            "teams repair"

        ]

        for phrase in bonus:

            if _normalize_text(phrase) in message:

                score += 50

    return score


# ============================================================
# TOTAL CONFIDENCE
# ============================================================

def calculate_confidence(
    message: str,
    application: str,
    issue: str,
) -> int:

    score = 0

    score += calculate_application_score(
        message,
        application
    )

    score += calculate_issue_score(
        message,
        issue
    )

    score = apply_bonus_rules(
        message,
        application,
        issue,
        score
    )

    return score

# ============================================================
# MAIN WORKFLOW SELECTOR
# ============================================================

def select(user_message: str) -> str:
    """
    Intelligent workflow selector.

    Flow:
        1. Normalize user message.
        2. Detect application (Teams / Outlook).
        3. Score every issue type.
        4. Pick the highest confidence workflow.
        5. Return Unknown if confidence is too low.
    """

    message = _normalize_text(user_message)

    if not message:
        return "Unknown"

    # --------------------------------------------------------
    # STEP 1 : Detect Application
    # --------------------------------------------------------

    application = detect_application(message)

    if application is None:
        return "Unknown"

    # --------------------------------------------------------
    # STEP 2 : Evaluate Every Issue
    # --------------------------------------------------------

    best_issue = None
    best_score = -1

    for issue in ISSUE_KEYWORDS.keys():

        # Teams has no Restart workflow? (future flexibility)
        if (application, issue) not in WORKFLOW_MAP:
            continue

        score = calculate_confidence(
            message,
            application,
            issue,
        )

        # ----------------------------------------------------
        # EXTRA SMART RULES
        # ----------------------------------------------------

        # "Outlook not working"
        if (
            application == "Outlook"
            and issue == "Launch"
            and (
                "not working" in message
                or "does not work" in message
                or "doesnt work" in message
                or "isnt working" in message
                or "not responding" in message
            )
        ):
            score += 100

        # "Teams not working"
        if (
            application == "Teams"
            and issue == "Launch"
            and (
                "not working" in message
                or "does not work" in message
                or "doesnt work" in message
                or "isnt working" in message
                or "not responding" in message
            )
        ):
            score += 100

        # Restart should win ONLY if restart words exist
        if (
            issue == "Restarting"
            and (
                "restart" in message
                or "restarting" in message
                or "restart loop" in message
                or "keeps restarting" in message
                or "keeps rebooting" in message
                or "keeps reopening" in message
            )
        ):
            score += 80

        # Update should win ONLY if update words exist
        if (
            issue == "Update"
            and (
                "update" in message
                or "updating" in message
                or "upgrade" in message
                or "version" in message
            )
        ):
            score += 80

        if score > best_score:

            best_score = score
            best_issue = issue

    # --------------------------------------------------------
    # STEP 3 : Confidence Check
    # --------------------------------------------------------

    if best_issue is None:
        return "Unknown"

    if best_score < 20:
        return "Unknown"

    # --------------------------------------------------------
    # STEP 4 : Return Workflow
    # --------------------------------------------------------

    return WORKFLOW_MAP[(application, best_issue)]