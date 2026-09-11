import json
from pathlib import Path

from tools.generate_figures import wiring

ROOT = Path(__file__).parents[1]


def test_wokwi_wiring_matches_firmware_pin_contract():
    pins = wiring()
    diagram = json.loads((ROOT / "wokwi/diagram.json").read_text(encoding="utf-8"))
    connections = {tuple(connection[:2]) for connection in diagram["connections"]}

    assert pins["DHT_PIN"] == 4
    assert pins["DS18B20_PIN"] == 15
    assert pins["GAS_PIN"] == 34
    assert pins["SD_CS"] == 5
    assert pins["I2C_SDA"] == 21
    assert pins["I2C_SCL"] == 22
    assert ("dht:SDA", "esp:D4") in connections
    assert ("ds18:DQ", "esp:D15") in connections
    assert ("bmp:SDA", "esp:D21") in connections
    assert ("bmp:SCL", "esp:D22") in connections
    assert ("gas:AO", "esp:D34") in connections
    assert ("sd:CS", "esp:D5") in connections
