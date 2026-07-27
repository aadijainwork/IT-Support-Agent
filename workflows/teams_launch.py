from utils.models import WorkflowContext

from automations.teams.installation import is_teams_installed
from automations.teams.executable import verify_executable
from automations.teams.disk import check_disk_space
from automations.teams.process import (
    stop_teams_process,
    start_teams_process
)
from automations.teams.cache import clear_teams_cache
from automations.teams.health import verify_launch
from automations.teams.diagnostics import (
    collect_diagnostics,
    save_diagnostics
)


def execute(context: WorkflowContext) -> WorkflowContext:
    """
    Executes the Microsoft Teams Launch Recovery workflow.

    Workflow

    1. Verify Teams installation.
    2. Verify executable.
    3. Stop running Teams processes.
    4. Clear Teams cache.
    5. Check disk space.
    6. Launch Teams.
    7. Verify launch.
    8. Collect diagnostics if launch fails.
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
    # Step 3 : Stop Existing Teams Processes
    # ------------------------------------------------------------

    stop_result = stop_teams_process()

    context.logs.append(stop_result["logs"])

    # ------------------------------------------------------------
    # Step 4 : Clear Teams Cache
    # ------------------------------------------------------------

    cache_result = clear_teams_cache()

    context.logs.append(cache_result["logs"])

    # ------------------------------------------------------------
    # Step 5 : Disk Space Check
    # ------------------------------------------------------------

    disk_result = check_disk_space()

    context.logs.append(disk_result["logs"])

    context.data["free_disk_space_gb"] = (
        disk_result.get("free_gb")
    )

    if not disk_result["success"]:

        context.logs.append(
            "Warning: Low disk space detected. "
            "Attempting to launch Teams anyway."
        )

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
            "Microsoft Teams could not be launched."
        )

        return context

    # ------------------------------------------------------------
    # Step 7 : Verify Launch
    # ------------------------------------------------------------

    health_result = verify_launch()

    context.logs.append(health_result["logs"])

    if not health_result["success"]:

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
            "Microsoft Teams failed to launch after all recovery attempts."
        )

        return context

    # ------------------------------------------------------------
    # Workflow Completed Successfully
    # ------------------------------------------------------------

    context.success = True

    context.data["teams_pid"] = (
        health_result.get("pid")
    )

    context.logs.append(
        "Microsoft Teams launched successfully."
    )

    return context