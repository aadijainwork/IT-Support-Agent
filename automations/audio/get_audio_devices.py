import json
import subprocess


def get_audio_devices():
    """Return currently present Windows audio devices."""

    command = r"""
    $devices = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Class -eq 'AudioEndpoint' -or
            $_.Class -eq 'MEDIA'
        } |
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
            return [devices]

        return devices if isinstance(devices, list) else []

    except Exception:
        return []