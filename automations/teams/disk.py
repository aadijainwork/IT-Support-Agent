import os
import shutil


MINIMUM_FREE_SPACE_GB = 2


def get_free_disk_space():
    """
    Returns the available disk space on the system drive.

    Returns:
        dict
    """

    try:

        system_drive = os.environ.get("SystemDrive", "C:")

        total, used, free = shutil.disk_usage(system_drive)

        free_gb = round(free / (1024 ** 3), 2)

        return {
            "success": True,
            "drive": system_drive,
            "free_gb": free_gb,
            "logs": f"Available disk space on {system_drive}: {free_gb} GB."
        }

    except Exception as e:

        return {
            "success": False,
            "drive": None,
            "free_gb": 0,
            "logs": f"Unable to determine free disk space. {str(e)}"
        }


def check_disk_space(minimum_required_gb=MINIMUM_FREE_SPACE_GB):
    """
    Verifies whether enough free disk space is available.

    Args:
        minimum_required_gb (float)

    Returns:
        dict
    """

    result = get_free_disk_space()

    if not result["success"]:
        return result

    if result["free_gb"] < minimum_required_gb:

        return {
            "success": False,
            "drive": result["drive"],
            "free_gb": result["free_gb"],
            "logs": (
                f"Insufficient disk space. "
                f"Available: {result['free_gb']} GB. "
                f"Minimum required: {minimum_required_gb} GB."
            )
        }

    return {
        "success": True,
        "drive": result["drive"],
        "free_gb": result["free_gb"],
        "logs": (
            f"Disk space check passed. "
            f"{result['free_gb']} GB available."
        )
    }