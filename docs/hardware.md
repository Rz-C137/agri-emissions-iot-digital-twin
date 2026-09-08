# Virtual hardware and interfaces

![Virtual hardware overview](figures/virtual_hardware_overview.svg)

Virtual hardware layout derived from the project wiring configuration. Component bodies and connector locations are schematic illustrations, not package pin order, mechanical dimensions or an assembly drawing.

![Exact connections](figures/esp32_pin_connections.svg)

The source is `wokwi/diagram.json`, checked against `firmware/include/Config.h` and the acquisition/storage modules. DHT22 DATA is GPIO4 with a 10 kΩ pull-up to 3.3 V; NC is unused. MQ-2 AO is ADC1 GPIO34; DO is unused. microSD CS is GPIO5, SCK GPIO18, DO/MISO GPIO19 and DI/MOSI GPIO23. The latter three are the Arduino ESP32 default SPI bus used by `SD.begin(Config::SD_CS)`.

DHT22 and microSD use 3.3 V and common GND. MQ-2 uses VIN/5 V and common GND in the simulator. Colors are for visual clarity only, not an electrical standard; signal net labels define the connection. Only endpoint/junction dots denote connections, not unmarked crossings.

![Component roles and named pins](figures/prototype_components.svg)

MQ-2 is used only to demonstrate an analog gas-acquisition channel. It is not treated as a selective NH₃ sensor. Firmware ADC acquisition leaves gas health UNVERIFIED even with a plausible voltage. Python's synthetic NH₃ instrument and fault status are separate.

## Physical front-end limitation

The virtual analog connection demonstrates the acquisition path. A physical implementation requires verification of sensor output voltage, ESP32 ADC input range, source impedance, filtering, protection and calibration. The direct 5 V-module AO connection is simulator-specific, not safe physical wiring by implication. Neither these figures nor Wokwi provide electrical validation. See [architecture](architecture.md) and [Wokwi notes](../wokwi/README.md).

![Conceptual measurement chain](figures/measurement_chain.svg)

Local logging and telemetry queueing are separate branches after QA/QC, not mutual prerequisites. The outage synchronization path is the controlled Python simulation. Firmware has bounded volatile RAM, optional SD logging and QoS 0 publishing; it does not guarantee delivery or replay SD records. Streamlit does not ingest live ESP32 telemetry. Physical validation has not occurred.

## Figure maintenance

The SVGs are original repository-owned illustrations under this project's MIT license, with no external image dependencies, branding, fonts or scripts. Regenerate with `python tools/generate_figures.py`. The generator checks the expected wiring and refuses stale pin assignments. It does not validate physical electronics. SVGs use standard text/path/shape primitives for crisp GitHub and browser rendering. Download or open at full width for individual pin labels on small screens.

No Wokwi runtime screenshot is supplied unless an actual successful runtime session is observed. See [verification](verification.md) for evidence and limitations.
