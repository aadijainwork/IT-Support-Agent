from utils.models import WorkflowContext

from automations.outlook.installation import is_outlook_installed
from automations.outlook.executable import verify_outlook_executable
from automations.outlook.runtime import detect_restart_loop
from automations.outlook.process import (
    stop_outlook_process,
    start_outlook_process
)
from automations.outlook.cache import clear_outlook_cache
from automations.outlook.health import verify_outlook_launch
from automations.outlook.diagnostics import (
    collect_outlook_diagnostics,
    save_outlook_diagnostics
)


def execute(context: WorkflowContext) -> WorkflowContext:
    """
    Executes the Microsoft Outlook Auto Restart Recovery workflow.

    Workflow

    1. Verify Outlook installation.
    2. Verify executable.
    3. Detect restart loop.
    4. Stop Outlook processes.
    5. Clear Outlook cache.
    6. Launch Outlook.
    7. Verify Outlook stability.
    8. Collect diagnostics if recovery fails.
    """

    installation_result = is_outlook_installed()
    context.logs.append(installation_result["logs"])

    if not installation_result["installed"]:
        context.success = False
        context.logs.append("Microsoft Outlook is not installed.")
        return context

    context.data["installation_path"] = installation_result.get("install_path")

    executable_result = verify_outlook_executable()
    context.logs.append(executable_result["logs"])

    if not executable_result["success"]:
        context.success = False
        context.logs.append("Microsoft Outlook executable verification failed.")
        return context

    context.data["outlook_executable"] = executable_result.get("path")

    restart_result = detect_restart_loop()
    context.logs.append(restart_result["logs"])

    if not restart_result["restart_detected"]:
        context.success = True
        context.logs.append("Microsoft Outlook is not experiencing an auto-restart issue.")
        return context

    context.data["restart_count"] = restart_result.get("restart_count")

    stop_result = stop_outlook_process()
    context.logs.append(stop_result["logs"])

    cache_result = clear_outlook_cache()
    context.logs.append(cache_result["logs"])

    start_result = start_outlook_process()
    context.logs.append(start_result["logs"])

    if not start_result["success"]:
        diagnostic_result = collect_outlook_diagnostics()
        context.logs.append(diagnostic_result["logs"])

        if diagnostic_result["success"]:
            save_result = save_outlook_diagnostics(diagnostic_result["diagnostics"])
            context.logs.append(save_result["logs"])
            context.data["diagnostics"] = diagnostic_result["diagnostics"]
            context.data["diagnostic_report"] = save_result.get("path")

        context.success = False
        context.logs.append("Microsoft Outlook could not be started.")
        return context

    stability_result = verify_outlook_launch()
    context.logs.append(stability_result["logs"])

    if not stability_result["success"]:
        diagnostic_result = collect_outlook_diagnostics()
        context.logs.append(diagnostic_result["logs"])

        if diagnostic_result["success"]:
            save_result = save_outlook_diagnostics(diagnostic_result["diagnostics"])
            context.logs.append(save_result["logs"])
            context.data["diagnostics"] = diagnostic_result["diagnostics"]
            context.data["diagnostic_report"] = save_result.get("path")

        context.success = False
        context.logs.append("Microsoft Outlook continues to restart unexpectedly after recovery.")
        return context

    context.success = True
    context.data["outlook_pid"] = stability_result.get("pid")
    context.logs.append("Microsoft Outlook is running normally and no longer restarting.")

    return context