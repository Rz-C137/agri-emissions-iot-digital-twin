from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_dashboard_all_pages_and_fault_controls():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "dashboard/app.py"))
    app.run(timeout=60)
    assert not app.exception
    for page in [
        "Live Monitoring",
        "System Architecture",
        "Fault Injection",
        "Data Quality",
        "Calibration & Validation",
        "Event Log",
        "Technical Details",
    ]:
        app.sidebar.radio[0].set_value(page).run(timeout=60)
        assert not app.exception, page
        if page == "Fault Injection":
            next(w for w in app.selectbox if w.label == "Inject a scenario").set_value(
                "NETWORK_OFFLINE"
            ).run()
            next(w for w in app.button if w.label == "Apply and acquire one sample").click().run()
            assert app.session_state["twin"].network == "OFFLINE"
