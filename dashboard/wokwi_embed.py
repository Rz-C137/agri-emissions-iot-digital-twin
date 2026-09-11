"""Expose the repository firmware and local simulation from Streamlit."""

import os
import subprocess
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
WOKWI_DIR = ROOT / "wokwi"
SOURCE_SUFFIXES = {".ino", ".h", ".cpp", ".txt"}
SKIP_FILES = {"README.md", "export.py"}


def _arduino_source_files() -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(WOKWI_DIR.iterdir()):
        if path.is_file() and path.suffix in SOURCE_SUFFIXES and path.name not in SKIP_FILES:
            files[path.name] = path.read_text(encoding="utf-8")
    return files


def _load_project_payload() -> dict[str, object] | None:
    diagram_path = WOKWI_DIR / "diagram.json"
    sketch_path = WOKWI_DIR / "sketch.ino"
    libraries_path = WOKWI_DIR / "libraries.txt"
    if not all(path.exists() for path in (diagram_path, sketch_path, libraries_path)):
        return None

    source_files = _arduino_source_files()
    if "sketch.ino" not in source_files or "libraries.txt" not in source_files:
        return None
    return {
        "diagram": diagram_path.read_text(encoding="utf-8"),
        "files": source_files,
    }


def _build_firmware() -> tuple[bool, str]:
    """Compile the ESP32 application locally and return concise build output."""
    try:
        result = subprocess.run(
            ["pio", "run", "-d", str(ROOT / "firmware")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=os.environ.copy(),
        )
    except OSError as error:
        return False, f"PlatformIO is unavailable: {error}"

    output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    return result.returncode == 0, "\n".join(output.splitlines()[-18:])


def render_wokwi_simulation() -> None:
    """Render the local firmware build and local Python simulation entry point."""
    payload = _load_project_payload()
    if payload is None:
        st.warning("Wokwi source files not found in `wokwi/`.")
        return

    st.info(
        "Local mode is enabled. The ESP32 firmware is compiled with PlatformIO on this machine; "
        "the dashboard simulation is the hardware-independent local twin."
    )

    with st.expander("Local ESP32 firmware", expanded=True):
        st.code("pio run -d firmware", language="powershell")
        if st.button("Compile firmware locally", type="primary"):
            with st.spinner("Compiling ESP32 firmware with PlatformIO..."):
                success, output = _build_firmware()
            if success:
                st.success("Firmware compiled locally.")
            else:
                st.error("Local firmware compilation failed.")
            st.code(output or "No build output.", language="text")

        artifact = ROOT / "firmware/.pio/build/esp32dev/firmware.bin"
        if artifact.exists():
            st.caption(f"Compiled artifact: `{artifact.relative_to(ROOT)}`")
        else:
            st.caption("No local firmware artifact yet. Compile it above.")

    st.markdown("#### Local simulation")
    st.success(
        "The local Python twin is running in the Overview page. Use **Run simulation** "
        "or **Advance 10 samples** in the sidebar."
    )
    st.markdown(
        "Wokwi browser execution is intentionally not used here because its experimental "
        "cloud API requires a firmware upload. The source project remains available in "
        "`wokwi/` for the documented browser workflow."
    )
    st.download_button(
        "Download diagram.json",
        payload["diagram"],
        file_name="diagram.json",
        mime="application/json",
    )

    with st.expander("Manual Wokwi setup", expanded=False):
        st.markdown(
            "Upload `wokwi/diagram.json`, `wokwi/sketch.ino`, and `wokwi/libraries.txt` "
            "into a new ESP32 project on wokwi.com."
        )
