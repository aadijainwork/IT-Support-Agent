import os
import winreg


def _check_outlook_registry() -> dict:
    """
    Inspects Windows Registry for Classic Microsoft Outlook and New Outlook installations.
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
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        except Exception:
                            pass

                        if "Outlook" in display_name or "Microsoft 365" in display_name or "Office" in display_name:
                            try:
                                display_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                            except Exception:
                                display_version = "Unknown"
                            try:
                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                            except Exception:
                                install_location = ""

                            return {
                                "installed": True,
                                "name": display_name,
                                "version": display_version,
                                "install_path": install_location,
                                "logs": f"Registry entry found for {display_name} (Version: {display_version})."
                            }
                    except Exception:
                        continue
            except Exception:
                continue

    return {
        "installed": False,
        "logs": "Microsoft Outlook installation not explicitly found in Windows Uninstall registry."
    }


def _check_common_outlook_paths() -> dict:
    """
    Checks standard filesystem paths for Classic Outlook and New Outlook.
    """
    possible_paths = [
        # Classic Outlook 64-bit / 32-bit Click-to-Run
        r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
        r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
        r"C:\Program Files\Microsoft Office\Office16\OUTLOOK.EXE",
        r"C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE",
        # New Outlook for Windows
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WindowsApps", "olk.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Packages", "Microsoft.OutlookForWindows_8wekyb3d8bbwe")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            is_new_outlook = "olk.exe" in path.lower() or "outlookforwindows" in path.lower()
            edition = "New Outlook" if is_new_outlook else "Classic Outlook"
            return {
                "installed": True,
                "edition": edition,
                "install_path": path,
                "logs": f"{edition} installation detected at: {path}"
            }

    return {
        "installed": False,
        "logs": "No Microsoft Outlook installation directory or executable found in standard locations."
    }


def is_outlook_installed() -> dict:
    """
    Determines whether Microsoft Outlook (Classic or New) is installed on the system.

    Returns:
        dict: Success status, installation path, edition info, and log messages.
    """
    path_result = _check_common_outlook_paths()
    if path_result["installed"]:
        return path_result

    registry_result = _check_outlook_registry()
    if registry_result["installed"]:
        return registry_result

    return {
        "installed": False,
        "install_path": None,
        "logs": "Microsoft Outlook installation could not be detected on this system."
    }


def get_outlook_installation_path() -> str | None:
    """
    Returns the detected Outlook installation path if available.
    """
    result = is_outlook_installed()
    if result["installed"]:
        return result.get("install_path")
    return None
