import json
import subprocess


def check_playback_endpoint():
    """Check whether Windows has at least one healthy playback endpoint."""

    command = r"""
    $devices = Get-PnpDevice -PresentOnly -Class AudioEndpoint -ErrorAction SilentlyContinue |
        Select-Object FriendlyName, InstanceId, Status, Class

    @($devices) | ConvertTo-Json -Depth 3 -Compress
    """

    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "available": False,
                "endpoints": [],
                "error": result.stderr.strip() or result.stdout.strip(),
            }

        output = result.stdout.strip()

        if not output:
            return {
                "success": True,
                "available": False,
                "endpoints": [],
            }

        devices = json.loads(output)
        if isinstance(devices, dict):
            devices = [devices]
        elif not isinstance(devices, list):
            devices = []

        endpoints = [
            device
            for device in devices
            if str(device.get("Status", "")).upper() == "OK"
        ]

        return {
            "success": True,
            "available": bool(endpoints),
            "endpoints": endpoints,
        }

    except Exception as exc:
        return {
            "success": False,
            "available": False,
            "endpoints": [],
            "error": str(exc),
        }