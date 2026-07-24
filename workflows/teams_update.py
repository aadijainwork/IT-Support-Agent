from utils.models import WorkflowContext
from automations.network.connectivity import check_teams_connectivity
from automations.teams.version import get_installed_teams_version
from automations.teams.process import stop_teams_process, start_teams_process
from automations.teams.update import trigger_teams_update
from automations.teams.cache import clear_teams_cache

def execute(context: WorkflowContext) -> WorkflowContext:
    """
    Executes production-quality Microsoft Teams Update workflow.
    Orchestrates network connectivity check, version detection, process shutdown,
    cache cleanup, package update/reset, verification, and restart.
    """
    # 1. Network Connectivity Check
    conn_result = check_teams_connectivity()
    context.logs.append(conn_result["logs"])
    if not conn_result["success"]:
        context.success = False
        context.logs.append("Network check failed. Cannot reach Microsoft Teams update servers.")
        return context

    # 2. Inspect Installed Version
    version_result = get_installed_teams_version()
    context.logs.append(version_result["logs"])
    if not version_result["installed"]:
        context.success = False
        context.logs.append("Microsoft Teams installation was not found on this machine.")
        return context

    context.data["initial_version"] = version_result["version"]

    # 3. Stop Running Teams Process
    stop_result = stop_teams_process()
    context.logs.append(stop_result["logs"])

    # 4. Clear Local App Cache
    cache_result = clear_teams_cache()
    context.logs.append(cache_result["logs"])

    # 5. Perform Update / Package Repair
    update_result = trigger_teams_update()
    context.logs.append(update_result["logs"])
    if not update_result["success"]:
        context.success = False
        context.logs.append("Teams package update step encountered an error.")
        return context

    # 6. Verify Post-Update Version & Package Health
    post_version_result = get_installed_teams_version()
    context.logs.append(f"Post-update verification: Teams version {post_version_result.get('version')} status is {post_version_result.get('status')}.")
    context.data["final_version"] = post_version_result.get("version")

    # 7. Restart Teams Application
    start_result = start_teams_process()
    context.logs.append(start_result["logs"])

    context.success = True
    context.logs.append("Teams update workflow completed successfully.")
    return context
