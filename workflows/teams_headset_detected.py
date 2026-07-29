from automations.audio.check_audio_service import check_audio_service
from automations.audio.restart_audio_service import restart_audio_service

from automations.audio.check_audio_endpoint_service import (
    check_audio_endpoint_service,
)
from automations.audio.restart_audio_endpoint_service import (
    restart_audio_endpoint_service,
)

from automations.audio.detect_headset import detect_headset
from automations.audio.rescan_audio_devices import rescan_audio_devices

from automations.audio.check_audio_device_status import (
    check_audio_device_status,
)
from automations.audio.enable_audio_device import enable_audio_device
from automations.audio.restart_audio_device import restart_audio_device

from automations.teams.process import (
    stop_teams_process,
    start_teams_process,
)


def teams_headset_detected(context):

    actions = []

    # =========================================================
    # 1. CHECK WINDOWS AUDIO SERVICE
    # =========================================================

    audio_service = check_audio_service()

    if not audio_service.get("running"):

        actions.append("Windows Audio service is not running.")

        restart_result = restart_audio_service()

        if not restart_result.get("success"):
            return _finish(
                context,
                False,
                "AUDIO_SERVICE_ERROR",
                "Windows Audio service could not be started.",
                actions,
            )

        actions.append("Windows Audio service restarted.")


    # =========================================================
    # 2. CHECK AUDIO ENDPOINT BUILDER
    # =========================================================

    endpoint_service = check_audio_endpoint_service()

    if not endpoint_service.get("running"):

        actions.append(
            "Windows Audio Endpoint Builder is not running."
        )

        restart_result = restart_audio_endpoint_service()

        if not restart_result.get("success"):
            return _finish(
                context,
                False,
                "AUDIO_ENDPOINT_SERVICE_ERROR",
                "Audio Endpoint Builder could not be started.",
                actions,
            )

        actions.append(
            "Audio Endpoint Builder restarted."
        )


    # =========================================================
    # 3. DETECT HEADSET
    # =========================================================

    headset = detect_headset()

    if not headset.get("detected"):

        actions.append(
            "Headset not detected. Rescanning audio devices."
        )

        rescan = rescan_audio_devices()

        if not rescan.get("success"):
            actions.append(
                "Windows device rescan could not be completed."
            )

        headset = detect_headset()


    # =========================================================
    # 4. STILL NOT DETECTED
    # =========================================================

    if not headset.get("detected"):

        return _finish(
            context,
            False,
            "HEADSET_NOT_DETECTED",
            (
                "Windows does not detect the headset. "
                "Check the USB connection or Bluetooth connection "
                "and reconnect the device."
            ),
            actions,
        )


    device = headset.get("device")

    actions.append(
        f"Headset detected: {device.get('FriendlyName', 'Unknown')}"
    )


    # =========================================================
    # 5. CHECK DEVICE HEALTH
    # =========================================================

    status = check_audio_device_status(device)

    if not status.get("healthy"):

        actions.append(
            f"Headset device status: {status.get('status', 'UNKNOWN')}"
        )

        # First try enabling it.
        enable_result = enable_audio_device(device)

        if enable_result.get("success"):
            actions.append("Headset device enabled.")

        # Verify after enabling.
        status = check_audio_device_status(device)


    # =========================================================
    # 6. DEVICE STILL UNHEALTHY
    # =========================================================

    if not status.get("healthy"):

        actions.append(
            "Attempting headset device restart."
        )

        restart_result = restart_audio_device(device)

        if not restart_result.get("success"):
            return _finish(
                context,
                False,
                "HEADSET_DEVICE_ERROR",
                (
                    "Windows detects the headset, but the device "
                    "is unhealthy and automatic recovery failed."
                ),
                actions,
            )

        status = check_audio_device_status(device)


    # =========================================================
    # 7. VERIFY DEVICE
    # =========================================================

    if not status.get("healthy"):

        return _finish(
            context,
            False,
            "HEADSET_DEVICE_ERROR",
            (
                "The headset is detected but Windows still reports "
                "a device problem."
            ),
            actions,
        )

    actions.append("Headset is healthy in Windows.")


    # =========================================================
    # 8. REFRESH TEAMS
    # =========================================================

    try:
        stop_teams_process()
        start_teams_process()

        actions.append(
            "Teams restarted to refresh audio devices."
        )

    except Exception as exc:

        return _finish(
            context,
            False,
            "TEAMS_RESTART_ERROR",
            (
                "The headset is healthy in Windows, but Teams "
                "could not be restarted."
            ),
            actions + [str(exc)],
        )


    # =========================================================
    # 9. FINAL HEADSET CHECK
    # =========================================================

    final_detection = detect_headset()

    if not final_detection.get("detected"):

        return _finish(
            context,
            False,
            "HEADSET_LOST_AFTER_RESTART",
            "The headset is no longer detected by Windows.",
            actions,
        )


    final_status = check_audio_device_status(
        final_detection["device"]
    )

    if not final_status.get("healthy"):

        return _finish(
            context,
            False,
            "HEADSET_DEVICE_ERROR",
            "The headset became unhealthy after recovery.",
            actions,
        )


    return _finish(
        context,
        True,
        "HEADSET_DETECTED",
        (
            "The headset is detected and healthy. "
            "Teams has been restarted to refresh the device."
        ),
        actions,
    )


def _finish(context, success, diagnosis, message, actions):

    context.success = success
    context.data["diagnosis"] = diagnosis
    context.data["actions"] = actions
    for action in actions:
        if action not in context.logs:
            context.logs.append(action)
    context.logs.append(message)

    return context


def execute(context):
    """Workflow entrypoint used by workflow registry."""

    return teams_headset_detected(context)