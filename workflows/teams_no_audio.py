from automations.audio.check_audio_service import check_audio_service
from automations.audio.restart_audio_service import restart_audio_service

from automations.audio.check_audio_endpoint_service import (
    check_audio_endpoint_service,
)
from automations.audio.restart_audio_endpoint_service import (
    restart_audio_endpoint_service,
)

from automations.audio.get_playback_endpoints import (
    get_playback_endpoints,
)
from automations.audio.check_playback_endpoint import (
    check_playback_endpoint,
)

from automations.audio.check_audio_device_status import (
    check_audio_device_status,
)
from automations.audio.restart_audio_device import restart_audio_device

from automations.teams.process import (
    stop_teams_process,
    start_teams_process,
)


def teams_no_audio(context):

    actions = []

    # =========================================================
    # 1. WINDOWS AUDIO SERVICE
    # =========================================================

    audio_service = check_audio_service()

    if not audio_service.get("running"):

        actions.append(
            "Windows Audio service is not running."
        )

        result = restart_audio_service()

        if not result.get("success"):
            return _finish(
                context,
                False,
                "AUDIO_SERVICE_ERROR",
                "Windows Audio service could not be started.",
                actions,
            )

        actions.append(
            "Windows Audio service restarted."
        )


    # =========================================================
    # 2. AUDIO ENDPOINT BUILDER
    # =========================================================

    endpoint_service = check_audio_endpoint_service()

    if not endpoint_service.get("running"):

        actions.append(
            "Audio Endpoint Builder is not running."
        )

        result = restart_audio_endpoint_service()

        if not result.get("success"):
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
    # 3. GET PLAYBACK ENDPOINTS
    # =========================================================

    playback_devices = get_playback_endpoints()

    if not playback_devices:

        return _finish(
            context,
            False,
            "NO_PLAYBACK_DEVICE",
            (
                "Windows does not currently expose a healthy "
                "audio playback endpoint."
            ),
            actions,
        )


    # =========================================================
    # 4. CHECK PLAYBACK ENDPOINT
    # =========================================================

    playback = check_playback_endpoint()

    if not playback.get("available"):

        actions.append(
            "No healthy playback endpoint found."
        )

        # Attempt repair of playback candidates.
        for device in playback_devices:

            status = check_audio_device_status(
                device
            )

            if status.get("healthy"):
                continue

            repair = restart_audio_device(
                device
            )

            if repair.get("success"):
                actions.append(
                    "Playback audio device restarted."
                )


        playback = check_playback_endpoint()

        if not playback.get("available"):

            return _finish(
                context,
                False,
                "PLAYBACK_DEVICE_ERROR",
                (
                    "Windows audio playback endpoints are not "
                    "healthy after recovery."
                ),
                actions,
            )


    actions.append(
        "Windows playback endpoint is available."
    )


    # =========================================================
    # 5. RESTART TEAMS
    # =========================================================

    try:

        stop_teams_process()
        start_teams_process()

        actions.append(
            "Teams restarted to refresh playback devices."
        )

    except Exception as exc:

        return _finish(
            context,
            False,
            "TEAMS_RESTART_ERROR",
            (
                "Windows audio output is healthy, but Teams "
                "could not be restarted."
            ),
            actions + [str(exc)],
        )


    # =========================================================
    # 6. FINAL PLAYBACK CHECK
    # =========================================================

    final_playback = check_playback_endpoint()

    if not final_playback.get("available"):

        return _finish(
            context,
            False,
            "PLAYBACK_ENDPOINT_LOST",
            (
                "The Windows playback endpoint became unavailable "
                "after recovery."
            ),
            actions,
        )


    return _finish(
        context,
        True,
        "PLAYBACK_HEALTHY",
        (
            "Windows audio output is available and healthy, "
            "and Teams has been restarted."
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

    return teams_no_audio(context)