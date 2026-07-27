import time
import subprocess
import json

try:
    import psutil
except ImportError:
    psutil = None


TEAMS_PROCESS_NAMES = {
    "ms-teams.exe",
    "teams.exe"
}


def is_teams_running():
    """
    Checks whether Microsoft Teams is currently running.

    Returns:
        dict
    """

    if psutil is not None:

        try:

            for process in psutil.process_iter(["pid", "name"]):

                try:

                    process_name = process.info["name"]

                    if (
                        process_name and
                        process_name.lower() in TEAMS_PROCESS_NAMES
                    ):

                        return {
                            "success": True,
                            "running": True,
                            "pid": process.info["pid"],
                            "logs": (
                                f"Microsoft Teams is running "
                                f"(PID: {process.info['pid']})."
                            )
                        }

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess
                ):

                    continue

            return {
                "success": False,
                "running": False,
                "pid": None,
                "logs": "Microsoft Teams process is not running."
            }

        except Exception:

            pass

    ps_command = (
        "$proc = Get-Process -Name ms-teams, Teams "
        "-ErrorAction SilentlyContinue | "
        "Select-Object -First 1; "
        "if ($proc) { "
        "[PSCustomObject]@{ Running = $true; Id = $proc.Id } "
        "| ConvertTo-Json "
        "} else { "
        "[PSCustomObject]@{ Running = $false; Id = $null } "
        "| ConvertTo-Json "
        "}"
    )

    try:

        result = subprocess.run(

            [
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                ps_command
            ],

            capture_output=True,
            text=True,
            timeout=10

        )

        if result.returncode == 0 and result.stdout.strip():

            data = json.loads(result.stdout.strip())

            if data.get("Running"):

                pid = data.get("Id")

                return {
                    "success": True,
                    "running": True,
                    "pid": pid,
                    "logs": (
                        f"Microsoft Teams is running "
                        f"(PID: {pid})."
                    )
                }

        return {
            "success": False,
            "running": False,
            "pid": None,
            "logs": "Microsoft Teams process is not running."
        }

    except Exception as error:

        return {
            "success": False,
            "running": False,
            "pid": None,
            "logs": (
                "Unable to determine Teams process status. "
                f"{str(error)}"
            )
        }


def wait_for_teams_launch(timeout=15):
    """
    Waits for Teams to appear in the process list.

    Args:
        timeout (int)

    Returns:
        dict
    """

    start_time = time.time()

    while time.time() - start_time < timeout:

        result = is_teams_running()

        if result["running"]:

            return result

        time.sleep(1)

    return {
        "success": False,
        "running": False,
        "pid": None,
        "logs": (
            f"Microsoft Teams did not start "
            f"within {timeout} seconds."
        )
    }


def verify_launch():
    """
    Confirms that Teams launched successfully.

    Returns:
        dict
    """

    return wait_for_teams_launch()


def verify_stability(
    monitoring_duration=30,
    check_interval=2
):
    """
    Verifies that Microsoft Teams remains running without
    unexpectedly closing or restarting.

    Args:
        monitoring_duration (int)
        check_interval (int)

    Returns:
        dict
    """

    initial_result = is_teams_running()

    if not initial_result["running"]:

        return {
            "success": False,
            "running": False,
            "pid": None,
            "logs": "Microsoft Teams is not running."
        }

    initial_pid = initial_result["pid"]

    start_time = time.time()

    while time.time() - start_time < monitoring_duration:

        current_result = is_teams_running()

        if not current_result["running"]:

            return {
                "success": False,
                "running": False,
                "pid": None,
                "logs": (
                    "Microsoft Teams closed during "
                    "stability monitoring."
                )
            }

        if current_result["pid"] != initial_pid:

            return {
                "success": False,
                "running": True,
                "pid": current_result["pid"],
                "logs": (
                    "Microsoft Teams restarted during "
                    "stability monitoring."
                )
            }

        time.sleep(check_interval)

    return {
        "success": True,
        "running": True,
        "pid": initial_pid,
        "logs": (
            f"Microsoft Teams remained stable for "
            f"{monitoring_duration} seconds."
        )
    }