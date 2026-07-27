import os
import winreg


def _check_registry():
    """
    Checks the Windows Registry for Microsoft Teams installation.

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

                        if not display_name:
                            continue

                        # Ignore Office Add-in
                        if "Meeting Add-in" in display_name:
                            continue

                        # Accept only genuine Teams installations
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
                            "logs": (
                                f"Microsoft Teams installation detected "
                                f"({display_name})."
                            )
                        }

                    except Exception:
                        continue

            except Exception:
                continue

    return {
        "installed": False,
        "logs": "Microsoft Teams installation not found in Windows Registry."
    }


def _check_common_locations():
    """
    Checks common Microsoft Teams installation folders.

    Returns:
        dict
    """

    possible_paths = [

        # Classic Teams
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Microsoft",
            "Teams"
        ),

        # New Teams (MSIX)
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Packages",
            "MSTeams_8wekyb3d8bbwe"
        ),

        # Machine-wide installation
        r"C:\Program Files\Microsoft\Teams",

        # 32-bit installation
        r"C:\Program Files (x86)\Microsoft\Teams"
    ]

    for path in possible_paths:

        if os.path.isdir(path):

            return {
                "installed": True,
                "install_path": path,
                "logs": (
                    f"Microsoft Teams installation directory found at "
                    f"{path}."
                )
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
    Returns the Teams installation path.

    Returns:
        str | None
    """

    result = is_teams_installed()

    if result["installed"]:
        return result.get("install_path")

    return None