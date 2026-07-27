import os


def find_outlook_executable() -> dict:
    """
    Searches standard installation paths for Classic Outlook (OUTLOOK.EXE) or New Outlook (olk.exe).

    Returns:
        dict: Success status, executable path, and logs.
    """
    possible_paths = [
        # Classic Outlook Click-to-Run (64-bit & 32-bit)
        r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
        r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
        r"C:\Program Files\Microsoft Office\Office16\OUTLOOK.EXE",
        r"C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE",
        # New Outlook for Windows
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WindowsApps", "olk.exe")
    ]

    for path in possible_paths:
        if os.path.isfile(path):
            is_new = "olk.exe" in path.lower()
            edition = "New Outlook (olk.exe)" if is_new else "Classic Outlook (OUTLOOK.EXE)"
            return {
                "success": True,
                "path": path,
                "edition": edition,
                "logs": f"{edition} executable located at: {path}"
            }

    return {
        "success": False,
        "path": None,
        "edition": None,
        "logs": "Microsoft Outlook executable (OUTLOOK.EXE / olk.exe) could not be located."
    }


def verify_outlook_executable() -> dict:
    """
    Verifies that the Outlook executable exists, is non-zero size, and has execute permissions.

    Returns:
        dict: Verification result details and logs.
    """
    result = find_outlook_executable()
    if not result["success"]:
        return result

    executable = result["path"]
    try:
        if not os.access(executable, os.X_OK):
            return {
                "success": False,
                "path": executable,
                "logs": f"Outlook executable found at {executable} but execution permission is denied."
            }

        if os.path.getsize(executable) == 0:
            return {
                "success": False,
                "path": executable,
                "logs": f"Outlook executable at {executable} is corrupted (0-byte binary)."
            }

        return {
            "success": True,
            "path": executable,
            "edition": result.get("edition"),
            "logs": f"Outlook executable verified successfully: {executable}"
        }

    except Exception as e:
        return {
            "success": False,
            "path": executable,
            "logs": f"Failed to verify Outlook executable: {str(e)}"
        }


def get_outlook_executable_path() -> str | None:
    """
    Returns only the verified executable path.
    """
    result = find_outlook_executable()
    if result["success"]:
        return result["path"]
    return None
