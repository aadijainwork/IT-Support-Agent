import time
import psutil


TEAMS_PROCESS_NAMES = [
    "ms-teams.exe",
    "Teams.exe"
]


def is_teams_running():
    """
    Checks whether Microsoft Teams is currently running.

    Returns:
        dict
    """

    try:

        for process in psutil.process_iter(["pid", "name"]):

            try:

                process_name = process.info["name"]

                if process_name and process_name.lower() in [
                    p.lower() for p in TEAMS_PROCESS_NAMES
                ]:

                    return {
                        "success": True,
                        "running": True,
                        "pid": process.info["pid"],
                        "logs": f"Microsoft Teams is running (PID: {process.info['pid']})."
                    }

            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                continue

        return {
            "success": False,
            "running": False,
            "pid": None,
            "logs": "Microsoft Teams process is not running."
        }

    except Exception as e:

        return {
            "success": False,
            "running": False,
            "pid": None,
            "logs": f"Unable to determine Teams process status. {str(e)}"
        }


def wait_for_teams_launch(timeout=15):
    """
    Waits for Teams to appear in the process list.

    Args:
        timeout (int): Maximum wait time in seconds.

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
        "logs": f"Microsoft Teams did not start within {timeout} seconds."
    }


def verify_launch():
    """
    Confirms that Teams launched successfully.

    Returns:
        dict
    """

    return wait_for_teams_launch()