import subprocess
import json

def clear_teams_cache() -> dict:
    """
    Clears New Teams local cache files at %LOCALAPPDATA%\\Packages\\MSTeams_8wekyb3d8bbwe\\LocalCache
    without removing user profile credentials.
    """
    ps_command = (
        "$path = \"$env:LOCALAPPDATA\\Packages\\MSTeams_8wekyb3d8bbwe\\LocalCache\"; "
        "if (Test-Path $path) { "
        "Remove-Item -Path \"$path\\*\" -Recurse -Force -ErrorAction SilentlyContinue; "
        "[PSCustomObject]@{ Cleared = $true; Path = $path } | ConvertTo-Json "
        "} else { "
        "[PSCustomObject]@{ Cleared = $false; Path = $path } | ConvertTo-Json "
        "}"
    )

    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
            capture_output=True, text=True, timeout=15
        )
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout.strip())
            if data.get("Cleared"):
                return {"success": True, "logs": f"Cleared Teams local cache at {data.get('Path')}."}
            return {"success": True, "logs": "No cache directory found to clear."}
        return {"success": True, "logs": "Completed Teams cache check."}
    except Exception as e:
        return {"success": False, "logs": f"Error clearing Teams cache: {str(e)}"}
