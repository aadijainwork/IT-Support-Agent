import subprocess


def restart_audio_device(device):
    """Disable and re-enable an audio device, then verify."""

    instance_id = device.get("InstanceId")

    if not instance_id:
        return {
            "success": False,
            "error": "Missing InstanceId",
        }

    safe_id = str(instance_id).replace("'", "''")

    command = f"""
    try {{
        Disable-PnpDevice `
            -InstanceId '{safe_id}' `
            -Confirm:$false `
            -ErrorAction Stop

        Start-Sleep -Seconds 2

        Enable-PnpDevice `
            -InstanceId '{safe_id}' `
            -Confirm:$false `
            -ErrorAction Stop

        Start-Sleep -Seconds 2

        (Get-PnpDevice -InstanceId '{safe_id}').Status
    }}
    catch {{
        Write-Error $_.Exception.Message
        exit 1
    }}
    """

    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

        status = result.stdout.strip()

        return {
            "success": result.returncode == 0 and status.upper() == "OK",
            "status": status.upper(),
            "error": result.stderr.strip(),
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }