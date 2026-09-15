import ctypes
import os
import sys

def run_game(game_path, dll_dir=None):
    """
    Launches a LÖVE game from a directory or .love file using liblove.dll.
    
    :param game_path: Path to the .love file or game folder.
    :param dll_dir: Directory containing liblove.dll and dependent DLLs.
                    Defaults to the script's directory if not provided.
    :return: Exit code from love_run_game.
    """
    abs_game_path = os.path.abspath(game_path)
    if not os.path.exists(abs_game_path):
        raise FileNotFoundError(f"Game path does not exist: {abs_game_path}")

    # Default to current working directory or directory of this script if dll_dir isn't passed
    if dll_dir is None:
        dll_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        dll_dir = os.path.abspath(dll_dir)

    dll_path = os.path.join(dll_dir, "liblove.dll")
    if not os.path.exists(dll_path):
        # Fallback check for love.dll
        fallback_path = os.path.join(dll_dir, "love.dll")
        if os.path.exists(fallback_path):
            dll_path = fallback_path
        else:
            raise FileNotFoundError(f"LÖVE DLL not found in {dll_dir}")

    # Register DLL directory for sub-dependencies (SDL2.dll, etc.) in Python 3.8+
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(dll_dir)

    # Load the library
    try:
        love_lib = ctypes.CDLL(dll_path)
    except OSError as e:
        raise OSError(f"Failed to load DLL from {dll_path}. Ensure all dependencies (SDL2.dll, etc.) are in {dll_dir}. Error: {e}")

    # Configure function signature
    try:
        love_run_game = love_lib.love_run_game
        love_run_game.argtypes = [ctypes.c_char_p]
        love_run_game.restype = ctypes.c_int
    except AttributeError:
        raise AttributeError("Could not find exported symbol 'love_run_game' in DLL.")

    # Execute
    return love_run_game(abs_game_path.encode('utf-8'))


# Command-line entry point
def main():
    if len(sys.argv) < 2:
        print("Usage: python program.py <path_to_game.love_or_directory> [dll_directory]")
        sys.exit(1)

    game_path = sys.argv[1]
    dll_dir = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        exit_code = run_game(game_path, dll_dir=dll_dir)
        print(f"LÖVE exited with code: {exit_code}")
        sys.exit(exit_code)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()