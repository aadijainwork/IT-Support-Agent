import time
import subprocess
import json

try:
    import psutil
except ImportError:
    psutil = None

OUTLOOK_PROCESS_NAMES = [
    "OUTLOOK.exe",
    "olk.exe"
]


def is_outlook_running() -> dict:
    """
    Checks whether Microsoft Outlook (OUTLOOK.EXE or olk.exe) is currently running.

    Returns:
        dict: Success status, running boolean, PID, and logs.
    """
    if psutil is not None:
        try:
            for process in psutil.process_iter(["pid", "name"]):
                try:
                    process_name = process.info["name"]
                    if process_name and process_name.lower() in [
                        p.lower() for p in OUTLOOK_PROCESS_NAMES
                    ]:
                        return {
                            "success": True,
                            "running": True,
                            "pid": process.info["pid"],
                            "logs": f"Microsoft Outlook is running (PID: {process.info['pid']})."
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            return {
                "success": False,
                "running": False,
                "pid": None,
                "logs": "Microsoft Outlook process is not running."
            }
        except Exception:
            pass

    # Native PowerShell fallback
    ps_command = (
        "$proc = Get-Process -Name OUTLOOK, olk -ErrorAction SilentlyContinue | Select-Object -First 1; "
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
                    "logs": f"Microsoft Outlook is running (PID: {pid})."
                }
        return {
            "success": False,
            "running": False,
            "pid": None,
            "logs": "Microsoft Outlook process is not running."
        }
    except Exception as e:
        return {
            "success": False,
            "running": False,
            "pid": None,
            "logs": f"Unable to determine Outlook process status: {str(e)}"
        }


def wait_for_outlook_launch(timeout: int = 15) -> dict:
    """
    Waits up to `timeout` seconds for Outlook to appear in the running process list.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = is_outlook_running()
        if result["running"]:
            return result
        time.sleep(1)

    return {
        "success": False,
        "running": False,
        "pid": None,
        "logs": f"Microsoft Outlook did not appear in running processes within {timeout} seconds."
    }


def verify_outlook_launch() -> dict:
    """
    Confirms that Microsoft Outlook launched successfully.
    """
    return wait_for_outlook_launch()
