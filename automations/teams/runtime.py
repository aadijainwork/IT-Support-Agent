import os
import winreg


def check_webview2_runtime():
    """
    Checks whether Microsoft Edge WebView2 Runtime is installed.

    Returns:
        dict
    """

    registry_locations = [

        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\EdgeUpdate\Clients"
        ),

        (
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\EdgeUpdate\Clients"
        )
    ]

    WEBVIEW2_GUID = "{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"

    for root, path in registry_locations:

        try:

            key = winreg.OpenKey(root, path)
            subkey = winreg.OpenKey(key, WEBVIEW2_GUID)

            version, _ = winreg.QueryValueEx(subkey, "pv")

            return {
                "success": True,
                "installed": True,
                "version": version,
                "logs": f"Microsoft Edge WebView2 Runtime detected. Version: {version}"
            }

        except Exception:
            continue

    return {
        "success": False,
        "installed": False,
        "version": None,
        "logs": "Microsoft Edge WebView2 Runtime is not installed."
    }


def check_runtime_dependencies():
    """
    Verifies all runtime dependencies required by Teams.

    Returns:
        dict
    """

    webview_result = check_webview2_runtime()

    if not webview_result["success"]:

        return {
            "success": False,
            "logs": webview_result["logs"]
        }

    return {
        "success": True,
        "logs": "All required runtime dependencies are available."
    }