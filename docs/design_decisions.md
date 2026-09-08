# Design decisions

I kept the existing ESP32 acquisition demonstration because the advertisement does not prescribe a board. Replacing working modules with a longer component list would not establish measurement competence.

I added a narrow Modbus RTU reference emulator because industrial messages, register scaling, CRC rejection and missing-response handling are independently testable. Its register map is explicitly my fixture. I documented UART/RS-485 wiring separately rather than implying that a Python packet test validates electrical behavior.

I included N2O alongside NH3 and CH4 because it is part of MARVELA's published scope. The three-gas campaign exercises data handling, while the richer NH3 model remains the calibration benchmark. A single MQ-2 analog channel cannot provide selective measurements of these species.

I used two SQLite databases to distinguish committed node records from committed receiver records. Stable identifiers make retry after a lost acknowledgement idempotent. This is a desktop experiment; implementing bounded embedded flash storage needs a separate wear, capacity and power-interruption design.

I retained affine calibration and chronological validation. More model complexity is not justified by this artificial dataset. Coefficients now carry provenance and can be loaded without fitting again; descriptive agreement limits supplement RMSE without claiming physical uncertainty coverage.

I kept WiFi/MQTT as the existing optional network path. Ethernet could suit fixed powered installations; LoRaWAN could suit sparse, constrained payloads, but either needs a site/link/power assessment. Neither is claimed implemented. I²C pins are a reserved extension, not an invented requirement for a particular sensor.

I used licensed real component photographs for recognition and original diagrams for wiring. Stock component photos are not photographs of a prototype I assembled.
