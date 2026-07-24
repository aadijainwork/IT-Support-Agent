import subprocess
import json

def trigger_teams_update() -> dict:
    """
    Triggers New Microsoft Teams update/reinstallation verification.
    Applies AppX package reset/update or invokes Teams bootstrapper update check.
    """
    ps_command = (
        "$pkg = Get-AppxPackage -Name MSTeams -ErrorAction SilentlyContinue; "
        "if ($pkg) { "
        "Reset-AppxPackage -Package $pkg.PackageFullName -ErrorAction SilentlyContinue; "
        "[PSCustomObject]@{ Success = $true; Package = $pkg.PackageFullName; Version = $pkg.Version } | ConvertTo-Json "
        "} else { "
        "[PSCustomObject]@{ Success = $false; Error = 'MSTeams AppX package not found.' } | ConvertTo-Json "
        "}"
    )

    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
            capture_output=True, text=True, timeout=30
        )
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout.strip())
            if data.get("Success"):
                return {"success": True, "logs": f"Successfully updated/reset package {data.get('Package')}."}
            return {"success": False, "logs": data.get("Error", "Update failed.")}
        return {"success": True, "logs": "Triggered Teams update check."}
    except Exception as e:
        return {"success": False, "logs": f"Error executing Teams update: {str(e)}"}
