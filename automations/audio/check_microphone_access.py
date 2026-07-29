import subprocess


def check_microphone_access():
    """Check current-user Windows microphone privacy setting."""

    command = r"""
    $path = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone'

    if (-not (Test-Path $path)) {
        Write-Output 'UNKNOWN'
        exit
    }

    $value = (
        Get-ItemProperty `
            -Path $path `
            -Name Value `
            -ErrorAction SilentlyContinue
    ).Value

    if ($null -eq $value) {
        Write-Output 'UNKNOWN'
    }
    else {
        Write-Output $value
    }
    """

    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "allowed": None,
                "status": "UNKNOWN",
                "error": result.stderr.strip(),
            }

        status = result.stdout.strip().upper()

        return {
            "success": True,
            "allowed": (
                True if status == "ALLOW"
                else False if status == "DENY"
                else None
            ),
            "status": status,
        }

    except Exception as exc:
        return {
            "success": False,
            "allowed": None,
            "status": "UNKNOWN",
            "error": str(exc),
        }