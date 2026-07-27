import subprocess
import json
from automations.outlook.executable import get_outlook_executable_path


def stop_outlook_process() -> dict:
    """
    Safely terminates running Classic Outlook (OUTLOOK.EXE) and New Outlook (olk.exe) processes.
    """
    ps_command = (
        "$procs = Get-Process -Name OUTLOOK, olk -ErrorAction SilentlyContinue; "
        "if ($procs) { "
        "Stop-Process -Name OUTLOOK, olk -Force -ErrorAction SilentlyContinue; "
        "[PSCustomObject]@{ Stopped = $true; Count = $procs.Count } | ConvertTo-Json "
        "} else { "
        "[PSCustomObject]@{ Stopped = $true; Count = 0 } | ConvertTo-Json "
        "}"
    )

    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
            capture_output=True, text=True, timeout=15
        )
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout.strip())
            count = data.get("Count", 0)
            log_msg = f"Terminated {count} running Outlook process(es)." if count > 0 else "No active Outlook processes were running."
            return {"success": True, "stopped_count": count, "logs": log_msg}
        return {"success": True, "stopped_count": 0, "logs": "Outlook process status checked."}
    except Exception as e:
        return {"success": False, "stopped_count": 0, "logs": f"Failed to stop Outlook process: {str(e)}"}


def start_outlook_process(safe_mode: bool = False) -> dict:
    """
    Launches Microsoft Outlook. If safe_mode is True, attempts launch with '/safe' switch.
    Tries URI protocol handler (ms-outlook:) or direct executable invocation.
    """
    exe_path = get_outlook_executable_path()

    if safe_mode and exe_path and "OUTLOOK.EXE" in exe_path.upper():
        ps_command = (
            f"try {{ "
            f"Start-Process -FilePath '{exe_path}' -ArgumentList '/safe' -ErrorAction Stop; "
            f"[PSCustomObject]@{{ Success = $true; Mode = 'SafeMode' }} | ConvertTo-Json "
            f"}} catch {{ "
            f"[PSCustomObject]@{{ Success = $false; Error = $_.Exception.Message }} | ConvertTo-Json "
            f"}}"
        )
    elif exe_path:
        ps_command = (
            f"try {{ "
            f"Start-Process -FilePath '{exe_path}' -ErrorAction Stop; "
            f"[PSCustomObject]@{{ Success = $true; Mode = 'Normal' }} | ConvertTo-Json "
            f"}} catch {{ "
            f"Start-Process 'ms-outlook:' -ErrorAction Stop; "
            f"[PSCustomObject]@{{ Success = $true; Mode = 'Protocol' }} | ConvertTo-Json "
            f"}}"
        )
    else:
        ps_command = (
            "try { "
            "Start-Process 'ms-outlook:' -ErrorAction Stop; "
            "[PSCustomObject]@{ Success = $true; Mode = 'Protocol' } | ConvertTo-Json "
            "} catch { "
            "[PSCustomObject]@{ Success = $false; Error = $_.Exception.Message } | ConvertTo-Json "
            "}"
        )

    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
            capture_output=True, text=True, timeout=15
        )
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout.strip())
            if data.get("Success"):
                mode = data.get("Mode", "Normal")
                log_suffix = " in Safe Mode (/safe)" if mode == "SafeMode" else ""
                return {"success": True, "mode": mode, "logs": f"Launched Microsoft Outlook successfully{log_suffix}."}
            return {"success": False, "logs": f"Failed to launch Outlook: {data.get('Error')}"}
        return {"success": True, "logs": "Triggered Outlook launch process."}
    except Exception as e:
        return {"success": False, "logs": f"Error launching Outlook process: {str(e)}"}
