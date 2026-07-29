import json
import subprocess


def detect_headset():
    """Detect healthy audio endpoints without name-based keyword matching."""

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
            return {
                "success": True,
                "detected": False,
                "device": None,
                "devices": [],
            }

        devices = json.loads(result.stdout)

        if isinstance(devices, dict):
            devices = [devices]
        elif not isinstance(devices, list):
            devices = []

    except Exception:
        devices = []

    matches = []

    for device in devices:
        if str(device.get("Status", "")).upper() == "OK":
            matches.append(device)

    return {
        "success": True,
        "detected": bool(matches),
        "device": matches[0] if matches else None,
        "devices": matches,
    }