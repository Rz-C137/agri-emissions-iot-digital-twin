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


def render_wokwi_simulation(compact: bool = False) -> None:
    """Render the Wokwi circuit canvas and the local firmware handoff."""
    payload = _load_project_payload()
    if payload is None:
        st.warning("Wokwi source files not found in `wokwi/`.")
        return

    if not compact:
        st.info(
            "Compile the firmware locally, then use the official Wokwi editor workflow to run the binary with this diagram."
        )
        st.image(
            str(ROOT / "docs/figures/virtual_hardware_overview.svg"),
            caption="ESP32 hero node: DHT22, DS18B20, BMP180, MQ-2 and microSD",
            width="stretch",
        )

    firmware_container = (
        st.container() if compact else st.expander("Local ESP32 firmware", expanded=True)
    )
    with firmware_container:
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
            st.download_button(
                "Download firmware.bin for Wokwi",
                artifact.read_bytes(),
                file_name="firmware.bin",
                mime="application/octet-stream",
            )
        else:
            st.caption("No local firmware artifact yet. Compile it above.")

    if not compact:
        st.markdown("#### Run the compiled firmware in Wokwi")
    else:
        st.markdown("**Firmware handoff**")
    st.link_button("Open Wokwi ESP32 editor", "https://wokwi.com/projects/new/esp32")
    st.markdown(
        "In the editor, upload `wokwi/diagram.json`, then use **Upload Firmware and Start Simulation** "
        "and select the downloaded `firmware.bin`. This produces the live circuit and serial monitor "
        "shown in your reference image."
    )
    st.download_button(
        "Download diagram.json",
        payload["diagram"],
        file_name="diagram.json",
        mime="application/json",
    )

    if not compact:
        with st.expander("Manual Wokwi setup", expanded=False):
            st.markdown("Detailed setup is maintained in the root README under **Wokwi workflow**.")
