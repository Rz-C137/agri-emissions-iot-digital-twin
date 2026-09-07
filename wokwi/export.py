"""Copy the modular PlatformIO application into browser-compatible Arduino tabs."""

from pathlib import Path
from shutil import copyfile

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    for source in (ROOT / "firmware/include").glob("*.h"):
        if source.name != "secrets.h":
            copyfile(source, ROOT / "wokwi" / source.name)
    for source in (ROOT / "firmware/src").glob("*.cpp"):
        target = "sketch.ino" if source.name == "main.cpp" else source.name
        copyfile(source, ROOT / "wokwi" / target)


if __name__ == "__main__":
    main()
