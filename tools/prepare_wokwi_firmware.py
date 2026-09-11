"""Copy PlatformIO build artifacts into wokwi/ for browser simulation."""

import json
import subprocess
import sys
from pathlib import Path
from shutil import copy2

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "firmware" / ".pio" / "build" / "esp32dev"
TARGET = ROOT / "wokwi"
ESPTOOL = Path.home() / ".platformio" / "packages" / "tool-esptoolpy" / "esptool.py"


def _require_build_artifacts() -> tuple[Path, Path, Path, Path]:
    bin_src = BUILD / "firmware.bin"
    elf_src = BUILD / "firmware.elf"
    bootloader_src = BUILD / "bootloader.bin"
    partitions_src = BUILD / "partitions.bin"
    missing = [
        path.name
        for path in (bin_src, elf_src, bootloader_src, partitions_src)
        if not path.exists()
    ]
    if missing:
        raise SystemExit(
            "Firmware binaries not found. Build first:\n"
            "  python -m platformio run -d firmware -e esp32dev\n"
            f"Missing: {', '.join(missing)}"
        )
    return bin_src, elf_src, bootloader_src, partitions_src


def _merge_firmware(
    bootloader_src: Path, partitions_src: Path, bin_src: Path, merged_dst: Path
) -> None:
    if not ESPTOOL.exists():
        raise SystemExit(
            "esptool.py not found. Install PlatformIO ESP32 toolchain first:\n"
            "  python -m platformio run -d firmware -e esp32dev"
        )
    subprocess.run(
        [
            sys.executable,
            str(ESPTOOL),
            "--chip",
            "esp32",
            "merge_bin",
            "-o",
            str(merged_dst),
            "--flash_mode",
            "dio",
            "--flash_freq",
            "40m",
            "--flash_size",
            "4MB",
            "0x1000",
            str(bootloader_src),
            "0x8000",
            str(partitions_src),
            "0x10000",
            str(bin_src),
        ],
        check=True,
    )


def main() -> None:
    bin_src, elf_src, bootloader_src, partitions_src = _require_build_artifacts()
    TARGET.mkdir(parents=True, exist_ok=True)

    copy2(bin_src, TARGET / "firmware.bin")
    copy2(elf_src, TARGET / "firmware.elf")
    copy2(bootloader_src, TARGET / "bootloader.bin")
    copy2(partitions_src, TARGET / "partitions.bin")

    merged_dst = TARGET / "firmware-merged.bin"
    _merge_firmware(bootloader_src, partitions_src, bin_src, merged_dst)

    flasher_args = {
        "write_flash_args": [
            "--flash_mode",
            "dio",
            "--flash_size",
            "4MB",
            "--flash_freq",
            "40m",
        ],
        "flash_files": {
            "0x1000": "bootloader.bin",
            "0x8000": "partitions.bin",
            "0x10000": "firmware.bin",
        },
    }
    (TARGET / "flasher_args.json").write_text(
        json.dumps(flasher_args, indent=2) + "\n", encoding="utf-8"
    )

    (TARGET / "wokwi.toml").write_text(
        "[wokwi]\nversion = 1\nfirmware = 'flasher_args.json'\nelf = 'firmware.elf'\n",
        encoding="utf-8",
    )

    print(f"Copied {bin_src.name} ({bin_src.stat().st_size} bytes) -> {TARGET / 'firmware.bin'}")
    print(f"Copied {elf_src.name} -> {TARGET / 'firmware.elf'}")
    print(f"Wrote merged image -> {merged_dst} ({merged_dst.stat().st_size} bytes)")
    print(f"Wrote {TARGET / 'flasher_args.json'} and {TARGET / 'wokwi.toml'}")


if __name__ == "__main__":
    main()
