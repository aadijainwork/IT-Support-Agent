import json
import subprocess


def get_playback_endpoints():
    """Return healthy audio endpoint devices using local system query."""

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

        if result.returncode != 0 or not result.stdout.strip():
            return []

        devices = json.loads(result.stdout)

        if isinstance(devices, dict):
            devices = [devices]
        elif not isinstance(devices, list):
            return []

        return [
            device
            for device in devices
            if str(device.get("Status", "")).upper() == "OK"
        ]

    except Exception:
        return []