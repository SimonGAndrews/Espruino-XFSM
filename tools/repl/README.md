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

`run_service_coexistence.py` coordinates the two-board ESP32 BLE, WiFi, HTTPS,
and XFSM workload described in
[`docs/service-coexistence-testing.md`](../../docs/service-coexistence-testing.md).
`bench_support.py` contains its shared transport and cleanup operations.

These runners were brought into this repository from the project author's
earlier ESP32 bench work and are now maintained here under MPL-2.0. They do not
depend on the earlier repository.
