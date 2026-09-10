# MAKE ANY UNITY GAME PLAYABLE

import glob
import os
import shutil
import time
from pathlib import Path

system32_path = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "rundll32.exe")

target_path = os.path.join(os.getcwd(), "rundll32.exe")

try:
    if os.path.exists(system32_path):
        # Copy the file
        shutil.copy2(system32_path, target_path)
        print(f"Successfully copied rundll32.exe to: {target_path}")

        # Update the modification and access times to the current time
        current_time = time.time()
        os.utime(target_path, (current_time, current_time))
        print("Updated file timestamp to the current time.")
    else:
        print(f"Source file not found at: {system32_path}")

    current_dir = Path.cwd()

    data_dirs = [
        p for p in current_dir.iterdir() if p.is_dir() and p.name.endswith("_Data")
    ]

    for folder in data_dirs:
        target_dir = current_dir / "rundll32_Data"
        if folder.name != "rundll32_Data":
            if target_dir.exists():
                print(
                    f"Cannot rename '{folder.name}': 'rundll32_Data' already exists."
                )
            else:
                folder.rename(target_dir)
                print(f"Renamed folder '{folder.name}' to 'rundll32_Data'")
            break

    exe_files = list(current_dir.glob("*.exe"))

    if exe_files:
        first_exe = exe_files[0]
        new_filename = f"run_{first_exe.stem}.bat"
        new_file_path = current_dir / new_filename

        file_content = f"./rundll32 ./UnityPlayer.dll,UnityMain"

        with open(new_file_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        print(f"Created file '{new_filename}' based on '{first_exe.name}'")
    else:
        print("No .exe files found in the current directory.")
except Exception as e:
    print(f"Error: {e}")
    time.sleep(3)