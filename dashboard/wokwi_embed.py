"""Embed the repository Wokwi project inside Streamlit via the experimental API."""

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
WOKWI_DIR = ROOT / "wokwi"
EMBED_CLIENT_ID = "wokwi_client_agri_emissions_demo"
EMBED_HEIGHT = 720


def _load_project_files() -> tuple[str, str]:
    diagram = (WOKWI_DIR / "diagram.json").read_text(encoding="utf-8")
    sketch = (WOKWI_DIR / "sketch.ino").read_text(encoding="utf-8")
    return diagram, sketch


def render_wokwi_simulation() -> None:
    """Render an interactive Wokwi simulation loaded from this repository."""
    diagram, sketch = _load_project_files()
    diagram_json = json.dumps(diagram)
    sketch_json = json.dumps(sketch)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: #f5f7f9;
      color: #18303b;
    }}
    .toolbar {{
      display: flex;
      gap: 10px;
      align-items: center;
      padding: 10px 12px;
      background: #ffffff;
      border-bottom: 1px solid #dde5e9;
    }}
    button {{
      background: #127f80;
      color: white;
      border: none;
      border-radius: 6px;
      padding: 8px 14px;
      cursor: pointer;
      font-size: 14px;
    }}
    button.secondary {{
      background: #5b7080;
    }}
    button:disabled {{
      opacity: 0.55;
      cursor: not-allowed;
    }}
    .status {{
      font-size: 13px;
      color: #345464;
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.85fr);
      gap: 0;
      min-height: {EMBED_HEIGHT - 48}px;
    }}
    iframe {{
      width: 100%;
      height: {EMBED_HEIGHT - 48}px;
      border: 0;
      background: #eef3f6;
    }}
    .monitor {{
      border-left: 1px solid #dde5e9;
      background: #0f1720;
      color: #d9e2ec;
      display: flex;
      flex-direction: column;
      min-height: {EMBED_HEIGHT - 48}px;
    }}
    .monitor h3 {{
      margin: 0;
      padding: 10px 12px;
      font-size: 14px;
      background: #1b2833;
      border-bottom: 1px solid #2d3f4d;
    }}
    pre {{
      margin: 0;
      padding: 12px;
      flex: 1;
      overflow: auto;
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 12px;
      line-height: 1.45;
      font-family: Consolas, "Courier New", monospace;
    }}
    @media (max-width: 900px) {{
      .layout {{
        grid-template-columns: 1fr;
      }}
      iframe, .monitor {{
        min-height: 420px;
      }}
    }}
  </style>
</head>
<body>
  <div class="toolbar">
    <button id="start-btn" disabled>Start simulation</button>
    <button id="restart-btn" class="secondary" disabled>Restart</button>
    <span class="status" id="status">Connecting to Wokwi…</span>
  </div>
  <div class="layout">
    <iframe
      id="wokwi-embed"
      src="https://wokwi.com/experimental/embed?client_id={EMBED_CLIENT_ID}"
      allow="serial; clipboard-read; clipboard-write"
    ></iframe>
    <div class="monitor">
      <h3>Serial monitor</h3>
      <pre id="serial-output">Waiting for simulation…</pre>
    </div>
  </div>
  <script type="module">
    const diagram = {diagram_json};
    const sketch = {sketch_json};
    const statusEl = document.getElementById("status");
    const outputEl = document.getElementById("serial-output");
    const startBtn = document.getElementById("start-btn");
    const restartBtn = document.getElementById("restart-btn");
    let client = null;
    let connected = false;

    class MessagePortTransport {{
      constructor(port) {{
        this.port = port;
        this.port.onmessage = (event) => {{
          if (this.onMessage) this.onMessage(event.data);
        }};
        this.port.start();
      }}
      send(message) {{
        this.port.postMessage(message);
      }}
    }}

    class WokwiClient extends EventTarget {{
      constructor(transport) {{
        super();
        this.transport = transport;
        this.lastId = 0;
        this.pendingCommands = new Map();
        transport.onMessage = (message) => this.processMessage(message);
      }}
      async fileUpload(name, content) {{
        return this.sendCommand("file:upload", {{ name, text: content }});
      }}
      async simStart(params) {{
        return this.sendCommand("sim:start", params);
      }}
      async simRestart(opts = {{}}) {{
        return this.sendCommand("sim:restart", opts);
      }}
      async serialMonitorListen() {{
        return this.sendCommand("serial-monitor:listen");
      }}
      sendCommand(command, params) {{
        return new Promise((resolve, reject) => {{
          const id = String(this.lastId++);
          this.pendingCommands.set(id, [resolve, reject]);
          this.transport.send({{ type: "command", command, params, id }});
        }});
      }}
      processMessage(message) {{
        if (message.type === "hello") {{
          this.dispatchEvent(new CustomEvent("wokwi:connected", {{ detail: message }}));
          return;
        }}
        if (message.type === "event" && message.event === "serial-monitor:data") {{
          const bytes = new Uint8Array(message.payload.bytes || []);
          outputEl.textContent += new TextDecoder().decode(bytes);
          outputEl.scrollTop = outputEl.scrollHeight;
          return;
        }}
        if (message.type === "response") {{
          const pending = this.pendingCommands.get(message.id || "");
          if (!pending) return;
          this.pendingCommands.delete(message.id || "");
          if (message.error) {{
            pending[1](new Error(message.result?.message || "Wokwi command failed"));
          }} else {{
            pending[0](message.result);
          }}
        }}
      }}
    }}

    async function uploadProject() {{
      statusEl.textContent = "Uploading diagram and firmware from repository…";
      await client.serialMonitorListen();
      await client.fileUpload("diagram.json", diagram);
      await client.fileUpload("sketch.ino", sketch);
      statusEl.textContent = "Project loaded. Click Start simulation.";
      startBtn.disabled = false;
      restartBtn.disabled = false;
    }}

    async function startSimulation() {{
      outputEl.textContent = "";
      statusEl.textContent = "Starting simulation…";
      await client.simStart({{ firmware: "sketch.ino", elf: "sketch.ino" }});
      statusEl.textContent = "Simulation running";
    }}

    window.addEventListener("message", async (event) => {{
      if (!event.data || !event.data.port || connected) return;
      connected = true;
      client = new WokwiClient(new MessagePortTransport(event.data.port));
      client.addEventListener("wokwi:connected", async () => {{
        try {{
          await uploadProject();
        }} catch (error) {{
          statusEl.textContent = "Failed to load project: " + error.message;
        }}
      }});
    }});

    startBtn.addEventListener("click", async () => {{
      startBtn.disabled = true;
      try {{
        await startSimulation();
      }} catch (error) {{
        statusEl.textContent = "Start failed: " + error.message;
      }} finally {{
        startBtn.disabled = false;
      }}
    }});

    restartBtn.addEventListener("click", async () => {{
      try {{
        outputEl.textContent = "";
        await client.simRestart();
        statusEl.textContent = "Simulation restarted";
      }} catch (error) {{
        statusEl.textContent = "Restart failed: " + error.message;
      }}
    }});
  </script>
</body>
</html>"""

    components.html(html, height=EMBED_HEIGHT, scrolling=False)

    with st.expander("Open in Wokwi editor", expanded=False):
        st.markdown(
            "If the embedded simulator does not load, open the same project files directly in Wokwi:"
        )
        st.code(
            "1. https://wokwi.com/projects/new/esp32\n"
            "2. Paste wokwi/diagram.json into the diagram editor\n"
            "3. Paste wokwi/sketch.ino into the code editor\n"
            "4. Click Start Simulation",
            language="text",
        )
        st.caption(
            "The embedded view loads diagram.json and sketch.ino from this repository automatically. "
            "MQ-2 is a simulator-only analog surrogate, not a selective NH₃ sensor."
        )
