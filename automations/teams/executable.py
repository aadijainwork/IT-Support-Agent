import os


def find_teams_executable():
    """
    Searches common Microsoft Teams executable locations.

    Returns:
        dict
    """

    possible_paths = [

        # Classic Teams (per-user)
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
        r"C:\Program Files (x86)\Microsoft\Teams\current\Teams.exe",

        # New Teams (Windows App Execution Alias)
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Microsoft",
            "WindowsApps",
            "ms-teams.exe"
        )
    ]

    for path in possible_paths:

        if os.path.isfile(path):

            return {
                "success": True,
                "path": path,
                "logs": f"Microsoft Teams executable located at: {path}"
            }

    return {
        "success": False,
        "path": None,
        "logs": "Microsoft Teams executable could not be located."
    }


def verify_executable():
    """
    Verifies that the Microsoft Teams executable exists and
    can be executed.

    Returns:
        dict
    """

    result = find_teams_executable()

    if not result["success"]:
        return result

    executable = result["path"]

    try:

        if not os.path.exists(executable):

            return {
                "success": False,
                "path": executable,
                "logs": "Microsoft Teams executable does not exist."
            }

        if not os.access(executable, os.X_OK):

            return {
                "success": False,
                "path": executable,
                "logs": "Microsoft Teams executable exists but cannot be executed."
            }

        return {
            "success": True,
            "path": executable,
            "logs": "Microsoft Teams executable verified successfully."
        }

    except Exception as e:

        return {
            "success": False,
            "path": executable,
            "logs": f"Executable verification failed. {str(e)}"
        }


def get_executable_path():
    """
    Returns the Teams executable path.

    Returns:
        str | None
    """

    result = find_teams_executable()

    if result["success"]:
        return result["path"]

    return None