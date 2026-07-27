import os


def find_teams_executable():
    """
    Searches common Microsoft Teams executable locations.

    Returns:
        dict
    """

    possible_paths = [

        # New Microsoft Teams
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Microsoft",
            "WindowsApps",
            "ms-teams.exe"
        ),

        # Classic Teams
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Microsoft",
            "Teams",
            "current",
            "Teams.exe"
        ),

        # Machine-wide installation
        r"C:\Program Files\Microsoft\Teams\current\Teams.exe",

        # 32-bit installation
        r"C:\Program Files (x86)\Microsoft\Teams\current\Teams.exe"
    ]

    for path in possible_paths:

        if os.path.isfile(path):

            return {
                "success": True,
                "path": path,
                "logs": f"Teams executable found at: {path}"
            }

    return {
        "success": False,
        "path": None,
        "logs": "Microsoft Teams executable could not be located."
    }


def verify_executable():
    """
    Verifies that the Teams executable exists and is valid.

    Returns:
        dict
    """

    result = find_teams_executable()

    if not result["success"]:
        return result

    executable = result["path"]

    try:

        if not os.access(executable, os.X_OK):

            return {
                "success": False,
                "path": executable,
                "logs": "Teams executable exists but cannot be executed."
            }

        if os.path.getsize(executable) == 0:

            return {
                "success": False,
                "path": executable,
                "logs": "Teams executable is corrupted (0-byte file)."
            }

        return {
            "success": True,
            "path": executable,
            "logs": "Teams executable verified successfully."
        }

    except Exception as e:

        return {
            "success": False,
            "path": executable,
            "logs": f"Executable verification failed: {str(e)}"
        }


def get_executable_path():
    """
    Returns only the executable path.

    Returns:
        str | None
    """

    result = find_teams_executable()

    if result["success"]:
        return result["path"]

    return None