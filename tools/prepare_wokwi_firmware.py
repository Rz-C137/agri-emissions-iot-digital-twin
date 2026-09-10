"""Copy PlatformIO build artifacts into wokwi/ for browser simulation."""

from pathlib import Path
from shutil import copy2

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "firmware" / ".pio" / "build" / "esp32dev"
TARGET = ROOT / "wokwi"


def main() -> None:
    bin_src = BUILD / "firmware.bin"
    elf_src = BUILD / "firmware.elf"
    if not bin_src.exists() or not elf_src.exists():
        raise SystemExit(
            "Firmware binaries not found. Build first:\n"
            "  python -m platformio run -d firmware -e esp32dev"
        )
    TARGET.mkdir(parents=True, exist_ok=True)
    copy2(bin_src, TARGET / "firmware.bin")
    copy2(elf_src, TARGET / "firmware.elf")
    print(f"Copied {bin_src.name} ({bin_src.stat().st_size} bytes) -> {TARGET / 'firmware.bin'}")
    print(f"Copied {elf_src.name} -> {TARGET / 'firmware.elf'}")


if __name__ == "__main__":
    main()
