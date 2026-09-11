import os
import shutil
import time

# Locate the standard System32 directory where rundll32.exe resides
system32_path = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "SysWOW64", "rundll32.exe")

# Define the target path in the current working directory
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
except Exception as e:
    print(f"Error handling file: {e}")
    time.sleep(3)