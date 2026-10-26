# Constrained ARM Device Testing

## Espruino Pico

Build the reduced Pico profile from the Espruino integration checkout:

```bash
source scripts/provision.sh PICO_R1_3
unset DEBUG
make BOARD=PICO_R1_3 clean
make BOARD=PICO_R1_3 RELEASE=1 USE_XFSM=1 USE_JIT=0 USE_DEBUGGER=0 \
  USE_TAB_COMPLETE=0 USE_NETWORK_JS=0 \
  SETDEFINES=<(printf '%s\n' 'DEFINES += -DNO_VECTOR_FONT=1') -j2
```

The application binary is `bin/espruino_2vXX_pico_1r3.bin`; confirm the exact
name from the final Make output. The verified application address is
`0x08010000`.

The Pico bootloader requires manual button handling. Follow Espruino's
[firmware-update procedure](https://www.espruino.com/Firmware+Update), put the
board into its serial bootloader state, confirm the bootloader port rather than
a normal REPL is selected, and use the Web IDE's advanced **Flash from file**
operation with the locally built binary. Do not write the application binary
at `0x08000000`; that is the full-device base and would overwrite the
bootloader arrangement.

After flashing, release the bootloader button, reset or reconnect the board,
and wait for its normal USB serial port. Run tests at 115,200 baud:

```bash
python3 tools/repl/run_test.py xfsm/tests/test_shell.js \
  --port /dev/serial/by-id/DEVICE --baud 115200 --timeout 30 --show-raw
```

The earlier qualification used a temporary Python 3 adaptation of Espruino's
legacy STM32 loader. That temporary file was not retained and is not a current
project dependency. Do not reproduce its recorded `/tmp` command unless a
maintained Python 3 loader has first been selected and verified.

## MDBT42Q

Build the constrained Bluetooth DFU profile:

```bash
source scripts/provision.sh MDBT42Q
unset DEBUG
make BOARD=MDBT42Q clean
make BOARD=MDBT42Q RELEASE=1 DFU_UPDATE_BUILD=1 USE_XFSM=1 \
  USE_JIT=0 USE_DEBUGGER=0 USE_TAB_COMPLETE=0 USE_NETWORK_JS=0 USE_NFC=0 \
  SETDEFINES=<(printf '%s\n' 'DEFINES += -DNO_VECTOR_FONT=1') -j2
```

Use the DFU ZIP named by the final Make output. The verified method follows the
[nRF52 firmware-update
procedure](https://www.espruino.com/Firmware+Update) and uses the Espruino Web
IDE advanced **Flash from file** operation over a Bluetooth bootloader
connection:

1. Disconnect UART software and place the board in bootloader mode.
2. Connect the Web IDE to the bootloader Bluetooth device, not the normal
   Espruino advertisement.
3. Select the locally built DFU ZIP and wait for flashing to complete.
4. Power-cycle the board and reconnect its FTDI UART for testing.

The verified console used an FTDI FT232R adapter at 9,600 baud. Verify common
ground and cross TX/RX before interpreting silence as a firmware failure. Do
not connect two competing power sources. Resolve the adapter through
`/dev/serial/by-id` and pace uploads in small chunks:

```bash
python3 tools/repl/run_test.py xfsm/tests/test_shell.js \
  --port /dev/serial/by-id/FTDI_DEVICE --baud 9600 \
  --timeout 60 --show-raw
```

Large conformance programs may exhaust the finite JsVar pool merely by being
held as REPL source. The qualified procedure writes those programs to a
temporary Storage file, evaluates the flash-backed string, and erases the file
afterward. This is test-loading control, not an XFSM runtime requirement.

## Qualification Notes

Always restore the exact production image after `XFC_MEASURE=1` or
`XFC_TEST=1`, verify that private hooks are absent, and confirm that temporary
Storage files are gone. The MDBT42Q profile has little flash margin, so rebuild
and recheck capacity after any engine or upstream Espruino growth.

The detailed historical measurements remain in the
[Pico](reports/2026-09-29-m8-pico-physical-qualification.md) and
[MDBT42Q](reports/2026-09-29-m8-mdbt42q-physical-qualification.md) reports.
