import importlib
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import os
import subprocess
import time
import shutil

def find_procs_fast_suspend(target_path):
    target_name = os.path.basename(target_path).lower()
    normalized_target = os.path.normcase(os.path.abspath(target_path))
    matching_processes = []

    # Only fetch 'name' initially
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == target_name:
                # Only check full exe path if name matches
                if os.path.normcase(proc.exe()) == normalized_target:
                    if proc.status() != psutil.STATUS_STOPPED:
                        proc.suspend()
                        print("KOd", target_path)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def find_procs_fast_kill(target_path):
    target_name = os.path.basename(target_path).lower()
    normalized_target = os.path.normcase(os.path.abspath(target_path))
    matching_processes = []
    # Only fetch 'name' initially
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == target_name:
                proc.kill()
                print("Killed", target_path)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def show_error(msg):
    root = tk.Tk()
    root.withdraw()  # hide the main window
    messagebox.showerror("Dependency Installation Failed", msg)
    root.destroy()

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        show_error(f"Failed to install required package: {package}\n\nError:\n{e}")
        sys.exit(1)

def ensure_package(package):
    try:
        importlib.import_module(package)
    except ImportError:
        install(package)

ensure_package("pystray")
ensure_package("pillow")
ensure_package("psutil")

import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item
import datetime
import time
from winreg import (HKEY_CURRENT_USER, KEY_QUERY_VALUE, KEY_SET_VALUE, OpenKey, QueryValueEx, REG_BINARY, SetValueEx)
import psutil

def dis_ib() -> None:
    with OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections', access=KEY_QUERY_VALUE | KEY_SET_VALUE) as connections:
        settings=bytearray(QueryValueEx(connections, 'DefaultConnectionSettings')[0])

        settings[0x4:0x8] = (int.from_bytes(settings[0x4:0x8], "little") + 1).to_bytes(4, "little")

        settings[0x8:0xc] = (0x1).to_bytes(4, "little")

        SetValueEx(connections, 'DefaultConnectionSettings', 0, REG_BINARY, bytes(settings))

def dis_clal() -> None:
    paths = ["%LOCALAPPDATA%/Microsoft/Edge/User Data/Default/Extensions/ojadkogjbnodmmefeihndccbjdhknljm", "%LOCALAPPDATA%/Google/Chrome/User Data/Default/Extensions/ihidolefpgnimlmgfljonacidpkmbhcl/"]
    for path in paths:
        print("Executing", path)
        expanded_path = os.path.expandvars(path)
        if os.path.exists(expanded_path) and os.path.isdir(expanded_path):
            try:
                shutil.rmtree(expanded_path)
                print(f"Successfully deleted: {expanded_path}")
            except Exception as e:
                print(f"Failed to delete directory: {e}")
        else:
            print(f"Directory not found: {expanded_path}")

def create_image(color):
    width = 64
    height = 64
    image = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((8,8,width-8,height-8), fill=color)
    return image

def on_exit(icon, item):
    icon.stop()
    os._exit(0)

def on_restart(icon, menu_item):
    icon.stop()
    subprocess.Popen([sys.executable] + sys.argv)
    os._exit(0)

running = True

def on_pause(icon, menu_item):
    global running
    running = not running  # toggle pause
    # change icon color
    icon.icon = create_image((255,165,0) if not running else (0,200,0))
    icon.update_menu()

if __name__ == "__main__":
    icon = pystray.Icon(
        "silly",
        create_image((255,165,0) if not running else (0,200,0)),
        "silly running",
        menu=pystray.Menu(
            item("Pause/Resume", on_pause),
            item("Restart", on_restart),
            item("Exit", on_exit)
        )
    )
    try:
        dis_clal()
    except Exception as e:
        pass
    threading.Thread(target=icon.run, daemon=True).start()
    while True:
        if running:
            dis_ib()
            find_procs_fast_suspend(r"C:\Program Files\Securly\Classroom\1.3.34.8\SlingshotApp.exe")
            find_procs_fast_kill(r"C:\Program Files\Securly\Classroom\Classroom.exe")
        time.sleep(0.2)
