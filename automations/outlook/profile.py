import winreg
from automations.outlook.process import start_outlook_process


def verify_outlook_profile() -> dict:
    """
    Inspects Windows Registry for Microsoft Outlook profile configuration.
    Checks HKCU\\Software\\Microsoft\\Office\\16.0\\Outlook\\Profiles.
    """
    profile_key_path = r"Software\Microsoft\Office\16.0\Outlook\Profiles"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, profile_key_path)
        subkeys_count = winreg.QueryInfoKey(key)[0]
        profiles = []
        for i in range(subkeys_count):
            try:
                profiles.append(winreg.EnumKey(key, i))
            except Exception:
                continue

        if profiles:
            return {
                "success": True,
                "has_profile": True,
                "profile_count": len(profiles),
                "profiles": profiles,
                "logs": f"Verified Outlook registry profiles ({len(profiles)} profile(s) found: {', '.join(profiles)})."
            }

        return {
            "success": True,
            "has_profile": False,
            "profile_count": 0,
            "profiles": [],
            "logs": "No Classic Outlook registry profiles detected under HKCU."
        }
    except Exception as e:
        return {
            "success": False,
            "has_profile": False,
            "profile_count": 0,
            "profiles": [],
            "logs": f"Outlook profile registry verification check skipped or not present: {str(e)}"
        }


def launch_outlook_safe_mode() -> dict:
    """
    Attempts to launch Microsoft Outlook in Safe Mode (/safe) to bypass failing COM add-ins.
    """
    return start_outlook_process(safe_mode=True)
