import ctypes
import ctypes.util
import subprocess


def set_volume(level: int):

    if level < 0 or level > 100:
        return "Volume must be between 0 and 100."

    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                f"set volume output volume {level}"
            ],
            check=True
        )

        return f"Volume set to {level}%."

    except subprocess.CalledProcessError:
        return "Failed to change system volume."

def mute():

    try:

        subprocess.run(
            [
                "osascript",
                "-e",
                "set volume output muted true",
                "-e",
                "set volume output volume 0"
            ],
            check=True
        )

        return "System muted."

    except subprocess.CalledProcessError:

        return "Failed to mute system."


def unmute():

    try:

        subprocess.run(
            [
                "osascript",
                "-e",
                "set volume output muted false",
                "-e",
                "set volume output volume 50"
            ],
            check=True
        )

        return "System unmuted."

    except subprocess.CalledProcessError:

        return "Failed to unmute system."


def set_brightness(level: int):
    if level < 0 or level > 100:
        return "Brightness must be between 0 and 100."

    try:
        # Load CoreGraphics for Main Display ID
        cg = ctypes.CDLL(
            ctypes.util.find_library("CoreGraphics")
            or "/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics"
        )
        cg.CGMainDisplayID.restype = ctypes.c_uint32
        display_id = cg.CGMainDisplayID()

        # Load DisplayServices for setting brightness on macOS (supports Apple Silicon & Intel)
        ds = ctypes.CDLL(
            ctypes.util.find_library("DisplayServices")
            or "/System/Library/PrivateFrameworks/DisplayServices.framework/DisplayServices"
        )
        ds.DisplayServicesSetLinearBrightness.argtypes = [ctypes.c_uint32, ctypes.c_float]
        ds.DisplayServicesSetLinearBrightness.restype = ctypes.c_int

        value = level / 100.0
        ret = ds.DisplayServicesSetLinearBrightness(display_id, ctypes.c_float(value))

        if ret == 0:
            return f"Brightness set to {level}%."
        return "Failed to change brightness."

    except Exception:
        # Fallback to brightness CLI if available
        try:
            value = level / 100.0
            subprocess.run(["brightness", str(value)], check=True, capture_output=True)
            return f"Brightness set to {level}%."
        except Exception:
            return "Failed to change brightness."

def lock_screen():
    try:
        login_framework = ctypes.cdll.LoadLibrary(
            "/System/Library/PrivateFrameworks/login.framework/login"
        )
        login_framework.SACLockScreenImmediate()
        return "Screen locked."
    except Exception:
        try:
            subprocess.run(["pmset", "displaysleepnow"], check=True)
            return "Screen locked."
        except Exception:
            return "Failed to lock screen."

if __name__ == "__main__":
    print(set_brightness(100))