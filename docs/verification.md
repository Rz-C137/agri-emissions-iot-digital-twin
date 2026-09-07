# Verification record

Checks performed on 2026-09-07 using Python 3.11 on Windows:

| Check | Observed result |
| --- | --- |
| Python tests | 10 passed, including all eight dashboard pages and network fault controls |
| Ruff lint | Passed |
| Ruff formatting | Passed |
| Deterministic generator | 4,320 rows plus calculated holdout metrics written |
| Streamlit server | Started successfully on localhost:8501 |
| Headless Edge browser | Overview and fault page rendered; no browser page errors |
| PlatformIO ESP32 build | Successful; RAM 50,440 bytes, flash 823,501 bytes |

The checked dataset's held-out raw RMSE is 2.2183 ppm and calibrated RMSE is 0.7102 ppm. These are calculated synthetic results, not physical accuracy claims. Full coefficients and metrics are in `data/demo.metrics.json`.

The meaningful tests cover deterministic reproducibility, disconnected/timed-out gas acquisition, local logging through a network outage, complete simulated queue synchronization, combined infrastructure faults, actual filesystem write errors, invalid/range/abrupt/outlier/stale flags, analytically known metrics and holdout leakage protection.

Not executed here: physical hardware tests, Wokwi browser simulation, credentialed ThingsBoard delivery, native C++ test execution (no host g++ available), or GitHub-hosted CI. The workflow includes the native test for a Linux runner. Build success establishes compilation, not hardware or browser runtime validation.

The browser screenshot is an actual local dashboard render of synthetic data. The project is ready for local use and repository review; account-dependent integrations have exact setup guides and remain optional.
