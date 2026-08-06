import subprocess


def restart_audio_endpoint_service():
    """Restart AudioEndpointBuilder and verify."""

    command = """
    try {
        Restart-Service -Name 'AudioEndpointBuilder' -Force -ErrorAction Stop
        Start-Sleep -Seconds 2

        (Get-Service -Name 'AudioEndpointBuilder').Status
    }
    catch {
        Write-Error $_.Exception.Message
        exit 1
    }
    """

    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )

        running = (
            result.returncode == 0
            and result.stdout.strip().lower() == "running"
        )

        return {
            "success": running,
            "running": running,
            "status": result.stdout.strip().upper(),
            "error": None if running else result.stderr.strip(),
        }

    except Exception as exc:
        return {
            "success": False,
            "running": False,
            "error": str(exc),
        }