import time
import subprocess
import json

try:
    import psutil
except ImportError:
    psutil = None


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
    if psutil is not None:
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
        except Exception:
            pass

    ps_command = (
        "$proc = Get-Process -Name ms-teams, Teams -ErrorAction SilentlyContinue | Select-Object -First 1; "
        "if ($proc) { "
        "[PSCustomObject]@{ Running = $true; Id = $proc.Id } | ConvertTo-Json "
        "} else { "
        "[PSCustomObject]@{ Running = $false; Id = $null } | ConvertTo-Json "
        "}"
    )
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
            capture_output=True, text=True, timeout=10
        )
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout.strip())
            if data.get("Running"):
                pid = data.get("Id")
                return {
                    "success": True,
                    "running": True,
                    "pid": pid,
                    "logs": f"Microsoft Teams is running (PID: {pid})."
                }
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