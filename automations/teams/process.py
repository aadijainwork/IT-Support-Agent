import subprocess
import json

def stop_teams_process() -> dict:
    """
    Safely terminates running New Teams (ms-teams.exe) and Classic Teams (Teams.exe) processes.
    """
    ps_command = (
        "$procs = Get-Process -Name ms-teams, Teams -ErrorAction SilentlyContinue; "
        "if ($procs) { "
        "Stop-Process -Name ms-teams, Teams -Force -ErrorAction SilentlyContinue; "
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
            log_msg = f"Terminated {count} running Teams process(es)." if count > 0 else "No active Teams processes were running."
            return {"success": True, "stopped_count": count, "logs": log_msg}
        return {"success": True, "stopped_count": 0, "logs": "Teams process status checked."}
    except Exception as e:
        return {"success": False, "stopped_count": 0, "logs": f"Failed to stop Teams process: {str(e)}"}

def start_teams_process() -> dict:
    """
    Launches New Microsoft Teams using the official 'msteams:' URI protocol handler.
    """
    ps_command = (
        "try { "
        "Start-Process 'msteams:' -ErrorAction Stop; "
        "[PSCustomObject]@{ Success = $true } | ConvertTo-Json "
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
                return {"success": True, "logs": "Launched Microsoft Teams via URI protocol (msteams:)."}
            return {"success": False, "logs": f"Failed to launch Teams: {data.get('Error')}"}
        return {"success": True, "logs": "Triggered Teams launch."}
    except Exception as e:
        return {"success": False, "logs": f"Error launching Teams process: {str(e)}"}
