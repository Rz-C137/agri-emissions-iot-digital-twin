from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_dashboard_all_pages_and_independent_controls():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "dashboard/app.py"))
    app.run(timeout=60)
    assert not app.exception
    app.sidebar.radio[0].set_value("Fault Injection").run()

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
        "Overview",
        "Live Monitoring",
        "System Architecture",
        "Virtual Hardware",
        "Commissioning Bench",
        "Data Quality",
        "Calibration & Validation",
        "Event Log",
        "Technical Details",
    ]:
        app.sidebar.radio[0].set_value(page).run(timeout=60)
        assert not app.exception, page
