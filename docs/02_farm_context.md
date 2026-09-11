# Farm Context

## Representative deployment scenario

The demonstrator represents a modular sensor node installed in a service or exhaust-adjacent area of an experimental livestock building. This is an **LVAT-like livestock research environment**, not a claim of access to the LVAT Gross Kreutz layout or infrastructure.

The node is intended to observe environmental and emission-related variables while remaining serviceable in dust, humidity, temperature variation, cable-routing constraints, and intermittent network conditions.

## Measurement problem

A research measurement system must acquire environmental variables and a gas-channel surrogate, preserve raw observations and quality flags, communicate with local and reference paths, and provide evidence for later calibration and validation.

The Phase 1 virtual node demonstrates interfaces and firmware flow. Agricultural NH3 selectivity, reference co-location, and field performance remain future physical work.

## Deployment concept

```text
representative barn environment
        -> ESP32 sensor node
        -> local QA/QC and microSD logging
        -> RS-485 reference-instrument path (bench/design stage)
        -> WiFi/MQTT transport (optional)
        -> storage and validation dashboard
```

Installation, enclosure, power, cable protection, contamination control, and maintenance must be confirmed during a physical bench and later field-design process.
