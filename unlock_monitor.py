import ctypes
import subprocess
import sys
import time
import os

def is_locked():
    user32 = ctypes.windll.User32
    return user32.GetForegroundWindow() == 0

EXE_PATH = os.path.join(os.path.dirname(sys.executable), 'face_unlock.exe')


last_launched = 0
cooldown = 30  # in seconds

while True:
    if is_locked():
        now = int(time.time())
        if now - last_launched > cooldown:
            print("[Monitor] System is locked. Launching Face Unlock.")
            try:
                subprocess.Popen([EXE_PATH])
                last_launched = now
            except FileNotFoundError as e:
                print(f"❌ Could not launch Face Unlock: {e}")
        else:
            print("[Monitor] Waiting to avoid duplicate launch.")
        time.sleep(5)
    else:
        time.sleep(5)
