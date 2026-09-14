# NOT MINE. Contribuited by [unknown, if you know who made this, please post an issue].
# -*- coding: utf_8 -*-

from __future__ import annotations

import sys
from ctypes import (CDLL, CFUNCTYPE, POINTER, byref, c_bool, c_int, c_size_t,
                    c_ubyte, c_uint, c_ulonglong, c_void_p, c_wchar_p, cast)
from os import chdir, system
from pathlib import Path
import struct
import os
import textwrap
import codecs

# Force UTF-8 on Windows to reduce garbling
if sys.platform == "win32":
    system('chcp 65001 > nul')
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def detect_pe_arch(exe_path: Path) -> str:
    """Detect if PE is 32-bit or 64-bit by reading headers."""
    with open(exe_path, 'rb') as f:
        # DOS header: e_lfanew at 0x3C
        f.seek(0x3C)
        e_lfanew = struct.unpack('<I', f.read(4))[0]
        
        # NT header signature
        f.seek(e_lfanew)
        sig = f.read(4)
        if sig != b'PE\0\0':
            raise ValueError("Invalid PE file")
        
        # Machine type (next 2 bytes)
        machine = struct.unpack('<H', f.read(2))[0]
        
        if machine == 0x014c:  # IMAGE_FILE_MACHINE_I386
            return '32'
        elif machine == 0x8664:  # IMAGE_FILE_MACHINE_AMD64
            return '64'
        else:
            raise ValueError(f"Unsupported machine type: 0x{machine:04x}")

DLL_PROCESS_ATTACH = c_uint(1)

def center_text(text: str, width: int) -> str:
    """Center a single line or multi-line text, wrapping if necessary."""
    wrapped_lines = []
    for line in text.splitlines():
        wrapped = textwrap.wrap(line, width=width - 4)  # Slight margin for safety
        for w_line in wrapped:
            padding = (width - len(w_line)) // 2
            wrapped_lines.append(' ' * padding + w_line)
    return '\n'.join(wrapped_lines)

def centered_print(text: str):
    """Print centered text in the console."""
    try:
        console_width = os.get_terminal_size().columns
    except:
        console_width = 80  # Default fallback
    print(center_text(text, console_width))

def centered_input(prompt: str) -> str:
    """Display centered prompt and get input on the same line."""
    try:
        width = os.get_terminal_size().columns
    except:
        width = 80
    padding = (width - len(prompt)) // 2
    full_prompt = ' ' * padding + prompt
    return input(full_prompt).strip()

def main() -> int:
    # Restored full original ASCII art with Unicode; adjusted third line of PROPANE block by moving back 1 space to fix warble
    ascii_art = textwrap.dedent(r'''
     PROPANE 


    ██████╗ ██████╗  ██████╗ ██████╗  █████╗ ███╗   ██╗███████╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗████╗  ██║██╔════╝
   ██████╔╝██████╔╝██║   ██║██████╔╝███████║██╔██╗ ██║█████╗  
   ██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  
    ██║     ██║  ██║╚██████╔╝██║     ██║  ██║██║ ╚████║███████╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ 


     ___ _  _ ___ _____ ___ _   _  ___ _____ ___ ___  _  _ ___ 
    |_ _| \| / __|_   _| _ \ | | |/ __|_   _|_ _/ _ \| \| / __| 
     | || .` \__ \ | | |   / |_| | (__  | |  | | (_) | .` \__ \ 
    |___|_|\_|___/ |_| |_|_\\___/ \___| |_| |___\___/|_|\_|___/ 

    ''')
    
    centered_print(ascii_art)

    instructions = "Place Propane.py in the folder with the exe you want to run. Type the name or number of the executable you want to run. Propane can only run x64 executables, x32 will not work."
    centered_print(instructions)

    argc_explanation = "argc (argument count) is the number of command-line arguments passed to a program (in C/C++ or similar), including the executable name as argv[0]. In this script, it's optional (default 0) and lets you specify extra args to pass when running the EXE, with argc incremented by 1 to include the EXE path."
    centered_print(argc_explanation)

    # Search current folder for .exe files
    current_dir = Path.cwd()
    exe_files = list(current_dir.glob('*.exe'))
    if not exe_files:
        centered_print("No Executable Found, please place Propane.py in the folder with the exe you want to run")
        centered_input("Press Enter to exit...")  # Centered pause to prevent instant closure
        return -1

    centered_print("Found .exe files:")
    exe_map = {}
    for i, exe_file in enumerate(exe_files, start=1):
        exe_map[str(i)] = exe_file
        centered_print(f"{i}: {exe_file.name}")

    # Prompt for Ignite: (number or filename/path)
    ignite_input = centered_input('Ignite: ')
    if ignite_input in exe_map:
        exe = exe_map[ignite_input].resolve()
    else:
        exe = Path(ignite_input).resolve()
    
    if not exe.exists() or not exe.suffix.lower() == '.exe':
        centered_print("Invalid EXE selection or not found. ")
        return -1

    # Detect arch (for validation; assume Python bitness matches)
    try:
        arch = detect_pe_arch(exe)
        centered_print(f"Detected {arch}-bit EXE. Ensure running with matching Python bitness! ")
    except ValueError as e:
        centered_print(f"Error: {e} ")
        return -1

    # Assume libPeConv in current dir (no prompt)
    peconv_dir = Path.cwd()
    if not (peconv_dir / 'libPeConv.dll').exists():
        centered_print("libPeConv.dll not found in current directory. ")
        return -1
    centered_print(f"Assuming libPeConv.dll in current directory is {arch}-bit. ")

    # Get argc/argv
    try:
        argc_input = centered_input('argc (optional, default 0): ') or '0'
        argc = int(argc_input)
        argv = []
        for i in range(argc):
            arg_input = centered_input(f'[{i + 1}] ')
            argv.append(arg_input)
        argc += 1  # Include argv[0] = exe
        argv = [str(exe)] + argv
    except ValueError:
        argc = 1
        argv = [str(exe)]

    peconv = CDLL(str(peconv_dir / 'libPeConv.dll'))

    # Load the PE
    load_pe_executable = peconv.load_pe_executable2
    load_pe_executable.restype = POINTER(c_ubyte)
    load_pe_executable.argtypes = (c_wchar_p, POINTER(c_size_t), c_void_p)
    size = c_size_t(0)
    pe: POINTER(c_ubyte) = load_pe_executable(str(exe), byref(size), None)

    if not pe:
        centered_print("Failed to load PE. ")
        return -1

    pe_addr = cast(pe, c_void_p)

    # Connect the PE to the PEB
    set_main_module_in_peb = peconv.set_main_module_in_peb
    set_main_module_in_peb.restype = c_bool
    set_main_module_in_peb.argtypes = (c_void_p,)
    if not set_main_module_in_peb(pe_addr):
        centered_print("Failed to set main module in PEB. ")
        return -1

    # Load delayed imports
    load_delayed_imports = peconv.load_delayed_imports
    load_delayed_imports.restype = c_bool
    load_delayed_imports.argtypes = (POINTER(c_ubyte), c_ulonglong, c_void_p)
    if not load_delayed_imports(pe, pe_addr.value, None):
        centered_print("Failed to load delayed imports. ")
        return -1

    # Run TLS callbacks
    run_tls_callbacks = peconv.run_tls_callbacks
    run_tls_callbacks.restype = c_size_t
    run_tls_callbacks.argtypes = (c_void_p, c_size_t, c_uint)
    run_tls_callbacks(pe_addr.value, size, DLL_PROCESS_ATTACH)

    # Calculate the entrypoint address
    get_entry_point_rva = peconv.get_entry_point_rva
    get_entry_point_rva.restype = c_uint
    get_entry_point_rva.argtypes = (POINTER(c_ubyte),)
    entry_rva: int = get_entry_point_rva(pe)

    if not entry_rva:
        centered_print("No entry point RVA found. ")
        return -2

    entry_va: int = pe_addr.value + entry_rva

    # Change to the executable's directory
    chdir(exe.parent)

    # Call the PE entrypoint
    return CFUNCTYPE(c_int, c_int, POINTER(c_wchar_p))(entry_va)(
        argc, (c_wchar_p * argc)(*argv)
    )

if __name__ == '__main__':
    sys.exit(main())