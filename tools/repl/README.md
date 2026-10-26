# Physical REPL Tools

These tools provide the host side of repeatable XFSM tests on Espruino boards.
They require Python 3 and the recorded
[`pyserial`](https://pyserial.readthedocs.io/en/latest/) version:

```bash
python3 -m pip install --user -r tools/repl/requirements.txt
```

`run_test.py` uploads one JavaScript test through a paced serial connection,
records the running board, Espruino version and Git revision, and returns a
failure status when the test emits a `FAIL ` line or omits its final `DONE=`
marker:

```bash
python3 tools/repl/run_test.py xfsm/tests/test_shell.js \
  --port /dev/serial/by-id/DEVICE --baud 115200 --timeout 30 --show-raw
```

Direct serial connections enable XON/XOFF flow control. Espruino can pause a
long UART upload while it processes input; runners and new bench tools must use
the shared `open_serial()` helper instead of opening an unregulated pyserial
connection.

`run_service_coexistence.py` coordinates the two-board ESP32 BLE, WiFi, HTTPS,
and XFSM workload described in
[`docs/service-coexistence-testing.md`](../../docs/service-coexistence-testing.md).
`bench_support.py` contains its shared transport and cleanup operations.

`run_qualification_suite.py` reads
`tests/device/qualification-manifest.json` and runs the applicable
production-firmware suites and canonical traces on one board. It records a JSON
summary when `--output` is supplied. It deliberately leaves measurement,
fault-injection, lifecycle, and multi-board service runs as separate firmware
or reset domains.

`run_lifecycle_test.py` runs the save/reboot/restoration fixture and its
subsequent `reset(true)` cleanup check as one reconnect-aware operation. Use it
instead of the ordinary single-test runner for `test_save_restore.js`.

These runners were brought into this repository from the project author's
earlier ESP32 bench work and are now maintained here under MPL-2.0. They do not
depend on the earlier repository.
