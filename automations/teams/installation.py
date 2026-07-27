import os
import winreg


def _check_registry():
    """
    Checks Windows Registry for Microsoft Teams installation.

    Returns:
        dict
    """
    uninstall_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):

        for uninstall_key in uninstall_keys:

            try:
                key = winreg.OpenKey(root, uninstall_key)

                for i in range(winreg.QueryInfoKey(key)[0]):

                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)

                        display_name = ""
                        display_version = ""
                        install_location = ""

                        try:
                            display_name = winreg.QueryValueEx(
                                subkey,
                                "DisplayName"
                            )[0]
                        except Exception:
                            pass

                        if "Teams" not in display_name:
                            continue

                        try:
                            display_version = winreg.QueryValueEx(
                                subkey,
                                "DisplayVersion"
                            )[0]
                        except Exception:
                            pass

                        try:
                            install_location = winreg.QueryValueEx(
                                subkey,
                                "InstallLocation"
                            )[0]
                        except Exception:
                            pass

                        return {
                            "installed": True,
                            "name": display_name,
                            "version": display_version,
                            "install_path": install_location,
                            "logs": f"Registry entry found for {display_name}."
                        }

                    except Exception:
                        continue

            except Exception:
                continue

    return {
        "installed": False,
        "logs": "Teams installation not found in Windows Registry."
    }


def _check_common_locations():
    """
    Checks common Microsoft Teams installation folders.

    Returns:
        dict
    """

    possible_paths = [

        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Microsoft",
            "Teams"
        ),

        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Packages",
            "MSTeams_8wekyb3d8bbwe"
        ),

        r"C:\Program Files\WindowsApps",

        r"C:\Program Files\Microsoft",

        r"C:\Program Files (x86)\Microsoft"
    ]

    for path in possible_paths:

        if os.path.exists(path):

            return {
                "installed": True,
                "install_path": path,
                "logs": f"Teams installation directory found at {path}."
            }

    return {
        "installed": False,
        "logs": "No Microsoft Teams installation directory found."
    }


def is_teams_installed():
    """
    Determines whether Microsoft Teams is installed.

    Returns:
        dict

        Example:

        {
            "installed": True,
            "version": "...",
            "install_path": "...",
            "logs": "..."
        }
    """

    registry_result = _check_registry()

    if registry_result["installed"]:
        return registry_result

    folder_result = _check_common_locations()

    if folder_result["installed"]:
        return folder_result

    return {
        "installed": False,
        "logs": (
            "Microsoft Teams installation could not be detected "
            "using Registry or common installation paths."
        )
    }


def get_installation_path():
    """
    Returns installation directory if available.

    Returns:
        str | None
    """

    result = is_teams_installed()

    if result["installed"]:
        return result.get("install_path")

    return None