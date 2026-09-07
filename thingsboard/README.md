# Optional ThingsBoard telemetry

The core dashboard never imports this publisher or contacts ThingsBoard. Use an existing free-tier entitlement only if available, or a self-hosted open-source ThingsBoard Community Edition deployment. Cloud plan names and quotas can change; no paid subscription or trial conversion is required for this project. If a free account is unavailable, skip this optional layer.

1. In your ThingsBoard instance, open **Entities → Devices**, add a device named `Virtual agricultural sensor`, and copy its access token from device credentials. Label the device and dashboard **SIMULATED**.
2. Read the instance's MQTT hostname and TLS port from its connection instructions. Do not assume the UI hostname is always the broker hostname.
3. Export `THINGSBOARD_HOST`, `THINGSBOARD_TOKEN` and optional `THINGSBOARD_PORT` (default 8883) into your shell environment. `.env.example` documents names but is not loaded automatically. Never commit a real token or paste it into a public Wokwi project.
4. Generate data using `python -m simulator` if needed, then explicitly send it:

```bash
python -m thingsboard.publish data/demo.csv
```

5. Open the device's **Latest telemetry** tab. Create optional time-series widgets for the fields below. The deterministic dataset uses January 2026 timestamps: select the corresponding historical time window rather than expecting records under a current-time dashboard view.

The publisher uses access-token authentication (token as MQTT username), TLS certificate verification, the established `v1/devices/me/telemetry` topic, QoS 1 and an atomic local progress checkpoint. A retry resumes an unchanged file. Checkpointing is not a multi-process queue: run one publisher per checkpoint. Delivery may duplicate a row after interruption; node/sequence and timestamp identify records within this dataset. Regenerating data changes source identity and restarts publication.

## Field mapping

| Telemetry key | Unit / interpretation |
| --- | --- |
| temperature_c | °C |
| relative_humidity_pct | % |
| gas_raw | Synthetic count-like surrogate |
| nh3_raw_ppm / nh3_calibrated_ppm / nh3_reference_ppm | ppm, entirely virtual |
| co2_ppm | ppm, synthetic |
| node_id / sequence | Source and attempt identity |
| sensor_status / network_status / storage_status | Acquisition-time states |
| quality_code / quality_flags | Shared bitmask and pipe-separated readable names |
| environmental_sensor_status / gas_channel_status | Separate channel diagnostics |
| timestamp_status | SIMULATED_UTC for this publisher |
| sensor_mode | Independent gas-fault selection |
| buffered | Acquired offline, not current queue status |
| scenario / simulated | Provenance; simulated is always true |
| split | Training or Validation in generated dataset |

Missing values are omitted because ThingsBoard telemetry values are typed scalars; their quality flags remain available. Top-level `ts` is epoch milliseconds converted from record UTC. Example shape, with illustrative synthetic numbers:

```json
{"ts":1767225600000,"values":{"node_id":"virtual-barn-01","sequence":0,"temperature_c":22.1,"relative_humidity_pct":69.5,"nh3_raw_ppm":9.2,"quality_code":0,"quality_flags":"VALID","simulated":true}}
```

Official references: [MQTT telemetry](https://thingsboard.io/docs/reference/mqtt-api/telemetry/) and [MQTT access-token authentication](https://thingsboard.io/docs/reference/mqtt-api/). These describe the service protocol; no live cloud execution is claimed in this repository.

See [schema contract](../docs/schema.md). The publisher rejects missing or timezone-naive UTC and emits strict JSON with nonfinite values omitted. Payload unit tests do not establish successful delivery to a broker.
