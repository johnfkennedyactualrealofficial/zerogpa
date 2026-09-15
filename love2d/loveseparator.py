import os
import sys

def unpackage_love_exe(fused_exe_path, output_exe_path="love.exe", output_love_path="Game.love"):
    if not os.path.exists(fused_exe_path):
        print(f"Error: File '{fused_exe_path}' not found.")
        return

    # Standard magic bytes for the start of a ZIP file header
    ZIP_SIGNATURE = b'PK\x03\x04'

    with open(fused_exe_path, "rb") as f:
        data = f.read()

    # Find the position where the ZIP archive begins
    zip_index = data.find(ZIP_SIGNATURE)

    if zip_index == -1:
        print("Error: Could not find a embedded .love (ZIP) archive inside this file.")
        return

    # Split the binary data into the original executable and the game archive
    exe_data = data[:zip_index]
    love_data = data[zip_index:]

    # Write out the separated love.exe
    with open(output_exe_path, "wb") as f:
        f.write(exe_data)
    print(f"Extracted executable to: {output_exe_path} ({len(exe_data)} bytes)")

    # Write out the separated Game.love
    with open(output_love_path, "wb") as f:
        f.write(love_data)
    print(f"Extracted game archive to: {output_love_path} ({len(love_data)} bytes)")

if __name__ == "__main__":
    input_file = "Balatro.exe"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
    unpackage_love_exe(input_file)