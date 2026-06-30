from pathlib import Path
import shutil

ASSETS_DIR = Path("assets")
OUTPUT_DIR = Path("output")


def copy_assets():

    destination = OUTPUT_DIR / "assets"

    if destination.exists():
        shutil.rmtree(destination)

    shutil.copytree(
        ASSETS_DIR,
        destination
    )

    print("Assets copied.")