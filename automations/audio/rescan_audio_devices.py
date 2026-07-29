import subprocess


def rescan_audio_devices():
    """Ask Windows Plug and Play to rescan hardware."""

    try:
        result = subprocess.run(
            ["pnputil.exe", "/scan-devices"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }