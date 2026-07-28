import time
import psutil


def detect_restart_loop(
    monitoring_duration=30,
    check_interval=2
):
    """
    Detects whether Microsoft Outlook is repeatedly restarting.

    Args:
        monitoring_duration (int):
            Total time (in seconds) to monitor Outlook.

        check_interval (int):
            Time (in seconds) between checks.

    Returns:
        dict
    """

    outlook_process_names = {
        "outlook.exe",
        "olk.exe"
    }

    restart_count = 0
    previous_pid = None
    ever_seen_running = False

    start_time = time.time()

    while time.time() - start_time < monitoring_duration:
        current_pid = None

        for process in psutil.process_iter(["pid", "name"]):
            try:
                process_name = process.info["name"]
                if process_name and process_name.lower() in outlook_process_names:
                    current_pid = process.info["pid"]
                    break
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        if current_pid is not None:
            ever_seen_running = True
            if previous_pid is None:
                previous_pid = current_pid
            elif current_pid != previous_pid:
                restart_count += 1
                previous_pid = current_pid

        time.sleep(check_interval)

    if not ever_seen_running:
        return {
            "success": False,
            "restart_detected": False,
            "restart_count": 0,
            "logs": "Microsoft Outlook is not currently running."
        }

    if restart_count > 0:
        return {
            "success": True,
            "restart_detected": True,
            "restart_count": restart_count,
            "logs": (
                f"Microsoft Outlook restarted "
                f"{restart_count} time(s) "
                f"during monitoring."
            )
        }

    return {
        "success": True,
        "restart_detected": False,
        "restart_count": 0,
        "logs": (
            "Microsoft Outlook remained stable "
            "during monitoring."
        )
    }