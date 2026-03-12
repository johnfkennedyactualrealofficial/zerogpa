"""Automatic installation management scripts"""

import urllib.request
import re
import os
import zipfile
import shutil
from pathlib import Path
import sys


OWNER = "eschan145"
REPO = "DieKnow"
BASE_DIR = Path(__file__).parent.resolve()
OUT = BASE_DIR / "_downloads"


def install():
    """Install DieKnow"""

    print("Installing DieKnow...")
    os.makedirs(OUT, exist_ok=True)

    release_page = f"https://github.com/{OWNER}/{REPO}/releases/latest"
    with urllib.request.urlopen(release_page) as response:
        final_url = response.geturl()

    match = re.search(r"/tag/([^/]+)$", final_url)
    if not match:
        raise RuntimeError("Could not determine latest release tag!")

    tag = match.group(1)

    zip_url = f"https://github.com/{OWNER}/{REPO}/archive/refs/tags/{tag}.zip"

    out_file = OUT / "_DieKnow.zip"
    print(f"Downloading {zip_url}...")
    urllib.request.urlretrieve(zip_url, out_file)
    print(f"Downloaded {out_file}")

    with zipfile.ZipFile(out_file, "r") as zip_ref:
        zip_ref.extractall()

    extracted_dir = f"{REPO}-{tag.lstrip('v')}"

    try:
        os.rename(extracted_dir, BASE_DIR / "DieKnow")
    except (FileExistsError, PermissionError):
        shutil.rmtree(BASE_DIR / "DieKnow")
        os.rename(extracted_dir, BASE_DIR / "DieKnow")

    shutil.rmtree(OUT)

    delete_result = input(
        "Extracted DieKnow folder. Should I delete development files? "
    )
    if delete_result.lower() not in ("y", "yes"):
        print("Installation completed successfully.")
        sys.exit()

    shutil.rmtree(BASE_DIR / "DieKnow/screenshots")
    shutil.rmtree(BASE_DIR / "DieKnow/tests")
    shutil.rmtree(BASE_DIR / "DieKnow/.github")
    shutil.rmtree(BASE_DIR / "DieKnow/docs")

    for file in Path(BASE_DIR / "DieKnow").rglob("*"):
        if file.suffix in {".cpp", ".h", ".md"}:
            file.unlink()

    junk = [
        ".gitattributes",
        ".gitignore",
        ".pylintrc",
        "CMakeLists.txt",
        "CPPCHECK.cfg",
        "README.md",
        "TROUBLESHOOTING.md",
        "windows.py",
        "manage.py"
    ]

    for path in junk:
        try:
            os.remove(BASE_DIR / "DieKnow" / path)
        except FileNotFoundError:
            continue

    print("Installation completed successfully.")


def uninstall(suicide=True):
    """
    Uninstall DieKnow. If `suicide` is True, the current file will be deleted
    as well.
    """

    print("Uninstalling currently installed version of DieKnow...")
    try:
        shutil.rmtree(BASE_DIR / "DieKnow")
    except FileNotFoundError:
        pass

    if suicide:
        os.remove(Path(__file__).resolve())

    print("Uninstalled DieKnow successfully.")


def update():
    """Uninstall and install DieKnow. The current script is maintained."""

    uninstall(False)
    install()


if "/install" in sys.argv:
    install()
elif "/uninstall" in sys.argv:
    uninstall()
elif "/update" in sys.argv:
    update()
else:

    def main():
        """Main loop"""
        result = input('Enter "install", "uninstall", or "update": ')
        match result:
            case "uninstall":
                uninstall()
            case "install":
                install()
            case "update":
                update()
            case _:
                print("Please enter a valid option")
                main()

    main()
