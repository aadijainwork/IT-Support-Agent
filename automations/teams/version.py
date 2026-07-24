import subprocess
import json
import time

def get_installed_teams_version(retries: int = 3, delay: float = 1.0) -> dict:
    """
    Inspects installed New Microsoft Teams AppX package (MSTeams).
    Retries up to `retries` times to account for background AppXSVC registration.
    """
    ps_command = (
        "$pkg = Get-AppxPackage -Name MSTeams -ErrorAction SilentlyContinue; "
        "if ($pkg) { "
        "[PSCustomObject]@{ Installed = $true; Version = $pkg.Version; PackageFullName = $pkg.PackageFullName; InstallLocation = $pkg.InstallLocation; Status = [string]$pkg.Status } | ConvertTo-Json "
        "} else { "
        "[PSCustomObject]@{ Installed = $false; Version = ''; PackageFullName = ''; InstallLocation = ''; Status = 'Not Installed' } | ConvertTo-Json "
        "}"
    )

    for attempt in range(retries):
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
                capture_output=True, text=True, timeout=15
            )
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout.strip())
                if data.get("Installed") or attempt == retries - 1:
                    return {
                        "success": data.get("Installed", False),
                        "installed": data.get("Installed", False),
                        "version": data.get("Version", ""),
                        "package_full_name": data.get("PackageFullName", ""),
                        "install_location": data.get("InstallLocation", ""),
                        "status": data.get("Status", ""),
                        "logs": f"Detected Microsoft Teams version: {data.get('Version')}" if data.get("Installed") else "Microsoft Teams AppX package is not installed."
                    }
        except Exception as e:
            if attempt == retries - 1:
                return {"success": False, "installed": False, "version": "", "logs": f"Error querying Teams version: {str(e)}"}
        time.sleep(delay)

    return {"success": False, "installed": False, "version": "", "logs": "Failed to query Teams AppX package."}
