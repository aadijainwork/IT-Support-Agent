import json
import subprocess


def check_audio_device_status(device):
    """Check PnP health of a specific audio device."""

    instance_id = device.get("InstanceId")

    if not instance_id:
        return {
            "success": False,
            "healthy": False,
            "status": "UNKNOWN",
            "error": "Missing InstanceId",
        }

    safe_id = str(instance_id).replace("'", "''")

    command = f"""
    $device = Get-PnpDevice -InstanceId '{safe_id}' -ErrorAction SilentlyContinue

    if ($null -eq $device) {{
        Write-Output 'NOT_FOUND'
    }}
    else {{
        $device |
            Select-Object FriendlyName, InstanceId, Status, Class |
            ConvertTo-Json -Compress
    }}
    """

    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        output = result.stdout.strip()

        if output == "NOT_FOUND":
            return {
                "success": True,
                "healthy": False,
                "status": "NOT_FOUND",
            }

        if result.returncode != 0:
            return {
                "success": False,
                "healthy": False,
                "status": "UNKNOWN",
                "error": result.stderr.strip(),
            }

        current_device = json.loads(output)
        status = str(current_device.get("Status", "UNKNOWN")).upper()

        return {
            "success": True,
            "healthy": status == "OK",
            "status": status,
            "device": current_device,
        }

    except Exception as exc:
        return {
            "success": False,
            "healthy": False,
            "status": "UNKNOWN",
            "error": str(exc),
        }