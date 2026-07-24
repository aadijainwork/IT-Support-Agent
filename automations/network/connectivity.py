import socket

def check_teams_connectivity() -> dict:
    """
    Verifies TCP connectivity to Microsoft Teams endpoints.
    Tries primary endpoints (config.teams.microsoft.com, teams.microsoft.com) with fallback.
    """
    targets = ["config.teams.microsoft.com", "teams.microsoft.com", "microsoft.com"]
    port = 443
    for target in targets:
        try:
            sock = socket.create_connection((target, port), timeout=3.0)
            sock.close()
            return {
                "success": True,
                "target": target,
                "address": target,
                "logs": f"Network check to {target}: Connected"
            }
        except Exception:
            continue

    return {
        "success": False,
        "target": targets[0],
        "logs": "Network check failed. Cannot reach Microsoft Teams servers."
    }
