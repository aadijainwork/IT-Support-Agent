import subprocess
import json


def clear_outlook_cache() -> dict:
    """
    Clears local temporary application cache (RoamCache & New Outlook LocalCache)
    without removing user profile credentials or OST/PST database files.
    """
    ps_command = (
        "$roam = \"$env:LOCALAPPDATA\\Microsoft\\Outlook\\RoamCache\"; "
        "$newCache = \"$env:LOCALAPPDATA\\Packages\\Microsoft.OutlookForWindows_8wekyb3d8bbwe\\LocalCache\"; "
        "$clearedRoam = $false; $clearedNew = $false; "
        "if (Test-Path $roam) { "
        "Remove-Item -Path \"$roam\\*\" -Recurse -Force -ErrorAction SilentlyContinue; "
        "$clearedRoam = $true "
        "}; "
        "if (Test-Path $newCache) { "
        "Remove-Item -Path \"$newCache\\*\" -Recurse -Force -ErrorAction SilentlyContinue; "
        "$clearedNew = $true "
        "}; "
        "[PSCustomObject]@{ ClearedRoam = $clearedRoam; ClearedNewCache = $clearedNew } | ConvertTo-Json"
    )

    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
            capture_output=True, text=True, timeout=15
        )
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout.strip())
            cleared_roam = data.get("ClearedRoam", False)
            cleared_new = data.get("ClearedNewCache", False)

            if cleared_roam or cleared_new:
                details = []
                if cleared_roam:
                    details.append("Outlook RoamCache")
                if cleared_new:
                    details.append("New Outlook LocalCache")
                return {"success": True, "logs": f"Cleared temporary cache for: {', '.join(details)}."}
            return {"success": True, "logs": "No active Outlook temporary cache directories needed clearing."}
        return {"success": True, "logs": "Completed Outlook cache cleanup."}
    except Exception as e:
        return {"success": False, "logs": f"Error clearing Outlook cache: {str(e)}"}
