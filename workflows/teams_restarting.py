from utils.models import WorkflowContext

from automations.teams.installation import is_teams_installed
from automations.teams.executable import verify_executable
from automations.teams.runtime import detect_restart_loop
from automations.teams.process import (
    stop_teams_process,
    start_teams_process
)
from automations.teams.cache import clear_teams_cache
from automations.teams.health import verify_stability
from automations.teams.diagnostics import (
    collect_diagnostics,
    save_diagnostics
)


def execute(context: WorkflowContext) -> WorkflowContext:
    """
    Executes the Microsoft Teams Auto Restart Recovery workflow.

    Workflow

    1. Verify Teams installation.
    2. Verify executable.
    3. Detect restart loop.
    4. Stop Teams processes.
    5. Clear Teams cache.
    6. Launch Teams.
    7. Verify Teams stability.
    8. Collect diagnostics if recovery fails.
    """

    # ------------------------------------------------------------
    # Step 1 : Verify Installation
    # ------------------------------------------------------------

    installation_result = is_teams_installed()

    context.logs.append(installation_result["logs"])

    if not installation_result["installed"]:

        context.success = False

        context.logs.append(
            "Microsoft Teams is not installed."
        )

        return context

    context.data["installation_path"] = (
        installation_result.get("install_path")
    )

    # ------------------------------------------------------------
    # Step 2 : Verify Executable
    # ------------------------------------------------------------

    executable_result = verify_executable()

    context.logs.append(executable_result["logs"])

    if not executable_result["success"]:

        context.success = False

        context.logs.append(
            "Microsoft Teams executable verification failed."
        )

        return context

    context.data["teams_executable"] = (
        executable_result.get("path")
    )

    # ------------------------------------------------------------
    # Step 3 : Detect Restart Loop
    # ------------------------------------------------------------

    restart_result = detect_restart_loop()

    context.logs.append(restart_result["logs"])

    if not restart_result["restart_detected"]:

        context.success = True

        context.logs.append(
            "Microsoft Teams is not experiencing an auto-restart issue."
        )

        return context

    context.data["restart_count"] = (
        restart_result.get("restart_count")
    )

    # ------------------------------------------------------------
    # Step 4 : Stop Teams Processes
    # ------------------------------------------------------------

    stop_result = stop_teams_process()

    context.logs.append(stop_result["logs"])

    # ------------------------------------------------------------
    # Step 5 : Clear Teams Cache
    # ------------------------------------------------------------

    cache_result = clear_teams_cache()

    context.logs.append(cache_result["logs"])

    # ------------------------------------------------------------
    # Step 6 : Launch Teams
    # ------------------------------------------------------------

    start_result = start_teams_process()

    context.logs.append(start_result["logs"])

    if not start_result["success"]:

        diagnostic_result = collect_diagnostics()

        context.logs.append(diagnostic_result["logs"])

        if diagnostic_result["success"]:

            save_result = save_diagnostics(
                diagnostic_result["diagnostics"]
            )

            context.logs.append(save_result["logs"])

            context.data["diagnostics"] = (
                diagnostic_result["diagnostics"]
            )

            context.data["diagnostic_report"] = (
                save_result.get("path")
            )

        context.success = False

        context.logs.append(
            "Microsoft Teams could not be started."
        )

        return context

    # ------------------------------------------------------------
    # Step 7 : Verify Stability
    # ------------------------------------------------------------

    stability_result = verify_stability()

    context.logs.append(stability_result["logs"])

    if not stability_result["success"]:

        diagnostic_result = collect_diagnostics()

        context.logs.append(diagnostic_result["logs"])

        if diagnostic_result["success"]:

            save_result = save_diagnostics(
                diagnostic_result["diagnostics"]
            )

            context.logs.append(save_result["logs"])

            context.data["diagnostics"] = (
                diagnostic_result["diagnostics"]
            )

            context.data["diagnostic_report"] = (
                save_result.get("path")
            )

        context.success = False

        context.logs.append(
            "Microsoft Teams continues to restart unexpectedly after recovery."
        )

        return context

    # ------------------------------------------------------------
    # Workflow Completed Successfully
    # ------------------------------------------------------------

    context.success = True

    context.data["teams_pid"] = (
        stability_result.get("pid")
    )

    context.logs.append(
        "Microsoft Teams is running normally and no longer restarting."
    )

    return context