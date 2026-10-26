# ESP32-C3 Device Testing

## Connection

The verified ESP32-C3 uses its native USB Serial/JTAG console and normally
appears as `ttyACM`. Find its persistent path each time the bench changes:

```bash
ls -l /dev/serial/by-id/ /dev/serial/by-path/
export ESP32C3_PORT=/dev/serial/by-id/REPLACE_WITH_ATTACHED_DEVICE
readlink -f "$ESP32C3_PORT"
fuser "$ESP32C3_PORT" || true
```

Close every process reported by `fuser` before flashing or testing. USB may
disconnect and enumerate again during reset; wait for the persistent link to
return before opening it.

## Build And Flash

Use the Espruino integration checkout, provision ESP-IDF 5 in a fresh shell,
and keep the stock 70 KB native-heap reserve:

```bash
cd /home/simon/Espruino-XFSM-Profile1
source scripts/provision.sh ESP32_IDF5
env -u DEBUG make BOARD=ESP32C3_IDF5 clean
env -u DEBUG make BOARD=ESP32C3_IDF5 RELEASE=1 USE_XFSM=1 -j2
env -u DEBUG make BOARD=ESP32C3_IDF5 RELEASE=1 USE_XFSM=1 \
  flash PORT="$ESP32C3_PORT"
```

Do not use the historical 65 KB `SETDEFINES` profile for normal firmware. It
was a diagnostic used before XFSM compiler metadata was reduced.

If flashing cannot enter the ROM loader, release the serial port, reconnect
USB, and retry. Use the board's BOOT and RESET controls only when automatic
entry still fails. Do not replace Espruino's Make target with guessed
`esptool` offsets.

## Runtime Check

After the USB console returns, query:

```javascript
print(JSON.stringify({
  board: process.env.BOARD,
  version: process.version,
  gitCommit: process.env.GIT_COMMIT,
  console: process.env.CONSOLE,
  createMachine: typeof require("XFSM").createMachine,
  privateMeasure: typeof require("XFSM")._measure
}));
```

The production image must report `ESP32C3_IDF5`, expose `createMachine`, and
leave `_measure` undefined. Then run a focused fixture using the common runner:

```bash
cd /home/simon/Espruino-XFSM
python3 tools/repl/run_test.py xfsm/tests/test_shell.js \
  --port "$ESP32C3_PORT" --baud 115200 --timeout 30 --show-raw
```

The complete Profile 2 history workload and the two-board service workload are
separate qualification steps. Follow
[Service-Coexistence Testing](service-coexistence-testing.md) when WiFi, BLE,
HTTPS, and XFSM must be active together.

The complete qualification runner loads canonical traces from a temporary
Storage file on ESP32-C3. This keeps the large `DIAG-006` and `COMPAT-006`
source text out of the finite JsVar pool while their machines execute. The
runner erases the temporary file after each trace.
