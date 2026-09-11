"""Copy the modular PlatformIO application into browser-compatible Arduino tabs."""

from pathlib import Path
from shutil import copyfile

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"main.cpp"}


def main() -> None:
    for source in (ROOT / "firmware/include").glob("*.h"):
        if source.name != "secrets.h":
            copyfile(source, ROOT / "wokwi" / source.name)
    for source in (ROOT / "firmware/src").glob("*.cpp"):
        if source.name in SKIP:
            copyfile(source, ROOT / "wokwi" / "sketch.ino")
        else:
            copyfile(source, ROOT / "wokwi" / source.name)


if __name__ == "__main__":
    main()
