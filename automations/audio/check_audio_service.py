import subprocess


def check_audio_service():
    """Check whether Windows Audio (Audiosrv) is running."""

    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                "(Get-Service -Name 'Audiosrv' -ErrorAction Stop).Status"
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "running": False,
                "status": "UNKNOWN",
                "error": result.stderr.strip(),
            }

        status = result.stdout.strip()

        return {
            "success": True,
            "running": status.lower() == "running",
            "status": status.upper(),
        }

    except Exception as exc:
        return {
            "success": False,
            "running": False,
            "status": "UNKNOWN",
            "error": str(exc),
        }