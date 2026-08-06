def is_audio_endpoint(device):
    """Return True when the device class is AudioEndpoint."""

    return str(device.get("Class", "")).lower() == "audioendpoint"


def is_healthy(device):
    """Return True when the device status is OK."""

    return str(device.get("Status", "")).upper() == "OK"


def filter_healthy_audio_endpoints(devices):
    """Return healthy AudioEndpoint devices from a raw device list."""

    return [
        device
        for device in devices
        if is_audio_endpoint(device) and is_healthy(device)
    ]