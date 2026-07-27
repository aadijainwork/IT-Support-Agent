import os
import platform
import socket
from datetime import datetime

from automations.outlook.installation import is_outlook_installed
from automations.outlook.executable import verify_outlook_executable
from automations.outlook.health import is_outlook_running
from automations.outlook.profile import verify_outlook_profile
from automations.teams.disk import get_free_disk_space


def collect_outlook_diagnostics() -> dict:
    """
    Collects Microsoft Outlook diagnostic information.
    """
    diagnostics = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "computer_name": socket.gethostname(),
        "operating_system": platform.platform()
    }

    installation = is_outlook_installed()
    executable = verify_outlook_executable()
    profile = verify_outlook_profile()
    disk = get_free_disk_space()
    health = is_outlook_running()

    diagnostics["outlook_installed"] = installation.get("installed")
    diagnostics["installation_path"] = installation.get("install_path")
    diagnostics["edition"] = installation.get("edition", "Unknown")

    diagnostics["executable_found"] = executable.get("success")
    diagnostics["executable_path"] = executable.get("path")

    diagnostics["profile_found"] = profile.get("has_profile")
    diagnostics["profiles_count"] = profile.get("profile_count")

    diagnostics["free_disk_space_gb"] = disk.get("free_gb")

    diagnostics["outlook_running"] = health.get("running")
    diagnostics["outlook_pid"] = health.get("pid")

    return {
        "success": True,
        "diagnostics": diagnostics,
        "logs": "Outlook diagnostic information collected successfully."
    }


def save_outlook_diagnostics(report: dict) -> dict:
    """
    Saves Outlook diagnostics into a text report.
    """
    try:
        reports_folder = "diagnostics"
        os.makedirs(reports_folder, exist_ok=True)

        filename = os.path.join(
            reports_folder,
            f"outlook_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(filename, "w", encoding="utf-8") as file:
            for key, value in report.items():
                file.write(f"{key}: {value}\n")

        return {
            "success": True,
            "path": filename,
            "logs": f"Outlook diagnostic report saved to {filename}"
        }

    except Exception as e:
        return {
            "success": False,
            "path": None,
            "logs": f"Unable to save Outlook diagnostic report: {str(e)}"
        }
