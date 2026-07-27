from utils.models import WorkflowContext
from automations.outlook.installation import is_outlook_installed
from automations.outlook.executable import verify_outlook_executable
from automations.outlook.process import stop_outlook_process, start_outlook_process
from automations.outlook.cache import clear_outlook_cache
from automations.outlook.profile import verify_outlook_profile, launch_outlook_safe_mode
from automations.outlook.health import verify_outlook_launch
from automations.outlook.diagnostics import collect_outlook_diagnostics, save_outlook_diagnostics
from automations.teams.disk import check_disk_space


def execute(context: WorkflowContext) -> WorkflowContext:
    """
    Executes production-quality Microsoft Outlook Launch Recovery workflow.

    Workflow Sequence (Microsoft Recommended):
    1. Verify Outlook installation.
    2. Verify executable integrity & permissions.
    3. Terminate hanging background processes.
    4. Clear temporary application cache & RoamCache.
    5. Verify sufficient system disk space.
    6. Inspect Outlook registry profile configuration.
    7. Attempt standard Outlook launch.
    8. Verify launch status.
    9. Fallback to Safe Mode (/safe) if normal launch fails.
    10. Collect diagnostics if all launch recovery attempts fail.
    """

    # Step 1: Verify Installation
    installation_result = is_outlook_installed()
    context.logs.append(installation_result["logs"])
    if not installation_result["installed"]:
        context.success = False
        context.logs.append("Microsoft Outlook installation was not found on this system.")
        return context

    context.data["installation_path"] = installation_result.get("install_path")
    context.data["edition"] = installation_result.get("edition")

    # Step 2: Verify Executable
    executable_result = verify_outlook_executable()
    context.logs.append(executable_result["logs"])
    if not executable_result["success"]:
        context.success = False
        context.logs.append("Microsoft Outlook executable verification failed.")
        return context

    context.data["executable_path"] = executable_result.get("path")

    # Step 3: Stop Hanging Processes
    stop_result = stop_outlook_process()
    context.logs.append(stop_result["logs"])

    # Step 4: Clear Temporary Cache
    cache_result = clear_outlook_cache()
    context.logs.append(cache_result["logs"])

    # Step 5: Check Disk Space (Reused from automations/teams/disk.py)
    disk_result = check_disk_space()
    context.logs.append(disk_result["logs"])
    if not disk_result["success"]:
        context.success = False
        context.logs.append("Insufficient disk space available for Outlook operation.")
        return context

    context.data["free_disk_space_gb"] = disk_result.get("free_gb")

    # Step 6: Verify Profile Registry
    profile_result = verify_outlook_profile()
    context.logs.append(profile_result["logs"])

    # Step 7: Attempt Standard Launch
    launch_result = start_outlook_process(safe_mode=False)
    context.logs.append(launch_result["logs"])

    # Step 8: Verify Launch
    health_result = verify_outlook_launch()
    context.logs.append(health_result["logs"])

    if health_result["running"]:
        context.success = True
        context.data["outlook_pid"] = health_result.get("pid")
        context.data["launch_mode"] = "Normal"
        context.logs.append("Microsoft Outlook launched successfully in Normal Mode.")
        return context

    # Step 9: Fallback to Safe Mode (/safe)
    context.logs.append("Normal launch unconfirmed. Attempting recovery launch in Safe Mode (/safe)...")
    safe_launch_result = launch_outlook_safe_mode()
    context.logs.append(safe_launch_result["logs"])

    safe_health_result = verify_outlook_launch()
    context.logs.append(safe_health_result["logs"])

    if safe_health_result["running"]:
        context.success = True
        context.data["outlook_pid"] = safe_health_result.get("pid")
        context.data["launch_mode"] = "SafeMode"
        context.logs.append("Microsoft Outlook launched successfully in Safe Mode.")
        return context

    # Step 10: Collect Diagnostics on Persistent Failure
    context.logs.append("Microsoft Outlook failed to launch after normal and Safe Mode attempts. Collecting diagnostics...")
    diag_result = collect_outlook_diagnostics()
    context.logs.append(diag_result["logs"])

    if diag_result["success"]:
        save_result = save_outlook_diagnostics(diag_result["diagnostics"])
        context.logs.append(save_result["logs"])
        context.data["diagnostics"] = diag_result["diagnostics"]
        context.data["diagnostic_report"] = save_result.get("path")

    context.success = False
    context.logs.append("Microsoft Outlook failed to launch after all recovery steps.")
    return context
