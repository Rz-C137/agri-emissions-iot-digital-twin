from simulator.sensor_validation import assess_temperature_agreement


def test_temperature_agreement_pass():
    result = assess_temperature_agreement(23.4, 23.2, 23.6, threshold_c=1.0)
    assert result["status"] == "PASS"
    assert result["flag"] == "VALID"
    assert result["max_disagreement_c"] <= 1.0


def test_temperature_agreement_detects_dht_fault():
    result = assess_temperature_agreement(29.0, 23.2, 23.4, threshold_c=1.0)
    assert result["status"] == "WARNING"
    assert result["flag"] == "TEMP_SENSOR_DISAGREEMENT"
    assert result["suspected_sensor"] == "DHT22"
