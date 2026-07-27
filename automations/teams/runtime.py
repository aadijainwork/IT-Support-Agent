import time
import psutil


def detect_restart_loop(
    monitoring_duration=30,
    check_interval=2
):
    """
    Detects whether Microsoft Teams is repeatedly restarting.

    Args:
        monitoring_duration (int):
            Total time (in seconds) to monitor Teams.

        check_interval (int):
            Time (in seconds) between checks.

    Returns:
        dict
    """

    teams_process_names = {

        "ms-teams.exe",
        "teams.exe"

    }

    restart_count = 0
    previous_pid = None

    start_time = time.time()

    while time.time() - start_time < monitoring_duration:

        current_pid = None

        for process in psutil.process_iter(

            ["pid", "name"]

        ):

            try:

                process_name = process.info["name"]

                if process_name and process_name.lower() in teams_process_names:

                    current_pid = process.info["pid"]
                    break

            except (

                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess

            ):

                continue

        # Teams not running
        if current_pid is None:

            return {

                "success": False,
                "restart_detected": False,
                "restart_count": restart_count,
                "logs": "Microsoft Teams is not currently running."

            }

        # First observation
        if previous_pid is None:

            previous_pid = current_pid

        # PID changed -> Teams restarted
        elif current_pid != previous_pid:

            restart_count += 1
            previous_pid = current_pid

        time.sleep(check_interval)

    if restart_count > 0:

        return {

            "success": True,
            "restart_detected": True,
            "restart_count": restart_count,
            "logs": (
                f"Microsoft Teams restarted "
                f"{restart_count} time(s) "
                f"during monitoring."
            )

        }

    return {

        "success": True,
        "restart_detected": False,
        "restart_count": 0,
        "logs": (
            "Microsoft Teams remained stable "
            "during monitoring."
        )

    }