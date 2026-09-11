from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_dashboard_three_pages_and_independent_controls():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "dashboard/app.py"))
    app.run(timeout=60)
    assert not app.exception

    app.sidebar.radio[0].set_value("🏠 Overview & Live System").run(timeout=60)
    assert not app.exception

    def click(label):
        next(w for w in app.button if w.label == label).click().run()
        assert not app.exception
        return app.session_state["twin"]

    click("Increase synthetic NH₃")
    twin = click("Disconnect network")
    assert twin.environment_mode == "HIGH_NH3"
    assert twin.pending
    click("Fail storage")
    twin = click("Restore network only")
    assert twin.network == "ONLINE" and twin.storage == "FAILED" and not twin.pending
    click("Apply gas fault")
    twin = click("Restore storage only")
    assert twin.storage == "OK" and twin.sensor_mode == "SENSOR_DISCONNECTED"
    twin = click("Restore sensor")
    assert twin.sensor_mode == "NORMAL" and twin.environment_mode == "HIGH_NH3"

    for page in [
        "🏠 Overview & Live System",
        "🧭 Bench-to-Barn Demonstrator",
        "🌡️ Sensor Commissioning",
        "🔧 Hardware & Architecture",
        "📊 Validation & Technical Details",
    ]:
        app.sidebar.radio[0].set_value(page).run(timeout=60)
        assert not app.exception, page

    app.sidebar.radio[0].set_value("🧭 Bench-to-Barn Demonstrator").run(timeout=60)
    assert any("Bench-to-Barn Engineering Demonstrator" in item.value for item in app.markdown)
    assert any("DHT22" in str(item.value) for item in app.dataframe)


def test_stale_twin_without_temp_fault_is_migrated():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "dashboard/app.py"))
    app.run(timeout=60)
    assert not app.exception

    class StaleTwin:
        records = [
            {
                "timestamp": "2026-01-01T00:00:00",
                "temperature_dht22_c": 20.0,
                "temperature_ds18b20_c": 20.1,
                "temperature_bmp180_c": 19.9,
                "temp_max_disagreement_c": 0.2,
            }
        ]

    app.session_state["twin"] = StaleTwin()
    app.sidebar.radio[0].set_value("🌡️ Sensor Commissioning").run(timeout=60)
    assert not app.exception
    assert hasattr(app.session_state["twin"], "set_temp_fault")
    assert app.session_state["twin"].temp_fault_mode == "NONE"
