import os
import platform
import socket
from datetime import datetime

from automations.teams.version import get_installed_teams_version
from automations.teams.installation import is_teams_installed
from automations.teams.executable import verify_executable
from automations.teams.disk import get_free_disk_space
from automations.teams.health import is_teams_running


def collect_diagnostics():
    """
    Collects Microsoft Teams diagnostic information.

    Returns:
        dict
    """

    diagnostics = {

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "computer_name": socket.gethostname(),

        "operating_system": platform.platform()
    }

    installation = is_teams_installed()
    executable = verify_executable()
    version = get_installed_teams_version()
    disk = get_free_disk_space()

    health = is_teams_running()

    diagnostics["teams_installed"] = installation.get("installed")
    diagnostics["installation_path"] = installation.get("install_path")

    diagnostics["teams_version"] = version.get("version")

    diagnostics["executable_found"] = executable.get("success")
    diagnostics["executable_path"] = executable.get("path")

    diagnostics["free_disk_space_gb"] = disk.get("free_gb")

    diagnostics["teams_running"] = health.get("running")
    diagnostics["teams_pid"] = health.get("pid")

    return {
        "success": True,
        "diagnostics": diagnostics,
        "logs": "Diagnostic information collected successfully."
    }


def save_diagnostics(report):

    """
    Saves diagnostics into a text report.

    Returns:
        dict
    """

    try:

        reports_folder = "diagnostics"

        os.makedirs(reports_folder, exist_ok=True)

        filename = os.path.join(
            reports_folder,
            f"teams_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(filename, "w", encoding="utf-8") as file:

            for key, value in report.items():

                file.write(f"{key}: {value}\n")

        return {

            "success": True,

            "path": filename,

            "logs": f"Diagnostic report saved to {filename}"
        }

    except Exception as e:

        return {

            "success": False,

            "path": None,

            "logs": f"Unable to save diagnostic report. {str(e)}"
        }