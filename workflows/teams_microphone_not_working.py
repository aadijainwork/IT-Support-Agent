from automations.audio.check_audio_service import check_audio_service
from automations.audio.restart_audio_service import restart_audio_service

from automations.audio.check_audio_endpoint_service import (
    check_audio_endpoint_service,
)
from automations.audio.restart_audio_endpoint_service import (
    restart_audio_endpoint_service,
)

from automations.audio.get_microphone_endpoints import (
    get_microphone_endpoints,
)
from automations.audio.check_microphone_endpoint import (
    check_microphone_endpoint,
)
from automations.audio.check_microphone_access import (
    check_microphone_access,
)

from automations.audio.check_audio_device_status import (
    check_audio_device_status,
)
from automations.audio.restart_audio_device import restart_audio_device

from automations.teams.process import (
    stop_teams_process,
    start_teams_process,
)


def teams_microphone_not_working(context):

    actions = []

    # =========================================================
    # 1. AUDIO SERVICE
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
    # 3. CHECK MICROPHONE ACCESS
    # =========================================================

    access = check_microphone_access()

    if access.get("allowed") is False:

        return _finish(
            context,
            False,
            "MICROPHONE_ACCESS_BLOCKED",
            (
                "Windows microphone access is disabled. "
                "Microphone access must be enabled before Teams "
                "can use the microphone."
            ),
            actions,
        )

    if access.get("allowed") is None:
        actions.append(
            "Microphone privacy status could not be determined."
        )


    # =========================================================
    # 4. GET MICROPHONE ENDPOINTS
    # =========================================================

    microphones = get_microphone_endpoints()

    if not microphones:

        return _finish(
            context,
            False,
            "MICROPHONE_NOT_DETECTED",
            (
                "Windows does not currently expose a microphone "
                "endpoint."
            ),
            actions,
        )


    # =========================================================
    # 5. CHECK MICROPHONE ENDPOINT
    # =========================================================

    microphone_check = check_microphone_endpoint()

    if microphone_check.get("available"):

        actions.append(
            "A healthy microphone endpoint is available."
        )

    else:

        actions.append(
            "No healthy microphone endpoint found."
        )

        # Try repairing microphone candidates individually.
        for microphone in microphones:

            status = check_audio_device_status(
                microphone
            )

            if status.get("healthy"):
                continue

            repair = restart_audio_device(
                microphone
            )

            if repair.get("success"):
                actions.append(
                    "Microphone audio device restarted."
                )


        # Recheck after attempted repair.
        microphone_check = check_microphone_endpoint()

        if not microphone_check.get("available"):

            return _finish(
                context,
                False,
                "MICROPHONE_DEVICE_ERROR",
                (
                    "A microphone device was found, but Windows "
                    "does not report a healthy microphone endpoint."
                ),
                actions,
            )


    # =========================================================
    # 6. WINDOWS MICROPHONE HEALTHY → RESTART TEAMS
    # =========================================================

    try:

        stop_teams_process()
        start_teams_process()

        actions.append(
            "Teams restarted to refresh microphone devices."
        )

    except Exception as exc:

        return _finish(
            context,
            False,
            "TEAMS_RESTART_ERROR",
            (
                "The microphone is available in Windows, but "
                "Teams could not be restarted."
            ),
            actions + [str(exc)],
        )


    # =========================================================
    # 7. FINAL CHECK
    # =========================================================

    final_check = check_microphone_endpoint()

    if not final_check.get("available"):

        return _finish(
            context,
            False,
            "MICROPHONE_LOST",
            (
                "The microphone endpoint is no longer available "
                "after recovery."
            ),
            actions,
        )


    return _finish(
        context,
        True,
        "MICROPHONE_HEALTHY",
        (
            "The microphone is available and healthy in Windows, "
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

    return teams_microphone_not_working(context)