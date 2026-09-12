import os
import sys
import subprocess
from pathlib import Path

LABEL = "com.aegis.assistant"

def get_plist_path():
    return Path(os.path.expanduser(f"~/Library/LaunchAgents/{LABEL}.plist"))

def get_log_dir():
    log_dir = Path(os.path.expanduser("~/.aegis"))
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def is_startup_enabled():
    return get_plist_path().exists()

def get_startup_status():
    plist_exists = is_startup_enabled()
    status = []
    status.append(f"LaunchAgent plist exists: {'Yes' if plist_exists else 'No'}")
    
    try:
        result = subprocess.run(["launchctl", "list", LABEL], capture_output=True, text=True)
        is_loaded = result.returncode == 0
        status.append(f"Loaded in launchd: {'Yes' if is_loaded else 'No'}")
        
        if is_loaded:
            for line in result.stdout.splitlines():
                if "PID" in line:
                    status.append(line.strip())
                elif "LastExitStatus" in line:
                    status.append(line.strip())
    except Exception as e:
        status.append(f"Could not query launchctl: {e}")
        
    return "\n".join(status)

def install_startup():
    plist_path = get_plist_path()
    log_dir = get_log_dir()
    
    project_dir = Path(__file__).parent.parent.absolute()
    app_py_path = project_dir / "app.py"
    
    python_exe = sys.executable
    
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_exe}</string>
        <string>{app_py_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{log_dir / 'daemon.log'}</string>
    <key>StandardErrorPath</key>
    <string>{log_dir / 'daemon_error.log'}</string>
    <key>WorkingDirectory</key>
    <string>{project_dir}</string>
</dict>
</plist>
"""
    
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    plist_path.write_text(plist_content)
    print(f"Created {plist_path}")
    
    # Reload
    subprocess.run(["launchctl", "unload", str(plist_path)], capture_output=True)
    result = subprocess.run(["launchctl", "load", str(plist_path)], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Startup successfully installed and loaded.")
    else:
        print(f"Failed to load startup agent: {result.stderr}")

def remove_startup():
    plist_path = get_plist_path()
    if not is_startup_enabled():
        print("Startup is already disabled (no plist found).")
        # Still attempt to unload just in case
        subprocess.run(["launchctl", "unload", str(plist_path)], capture_output=True)
        return
        
    print(f"Unloading {LABEL}...")
    subprocess.run(["launchctl", "unload", str(plist_path)], capture_output=True)
    
    try:
        plist_path.unlink()
        print(f"Removed {plist_path}")
    except Exception as e:
        print(f"Error removing plist: {e}")
        
    print("Startup successfully removed.")
