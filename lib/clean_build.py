from pathlib import Path
import shutil


OUTPUT_DIR = Path("output")


def clean_build():

    if OUTPUT_DIR.exists():

        print("Cleaning previous build...")

        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Output directory ready.")