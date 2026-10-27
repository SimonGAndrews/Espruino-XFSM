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

The normal build produces an application-only BIN for a loader that accepts an
explicit address. To produce the address-positioned BIN required by the Web
IDE's **Flash from file** operation, add `PAD_FOR_BOOTLOADER=1` to the clean
build:

```bash
make BOARD=PICO_R1_3 clean
make BOARD=PICO_R1_3 RELEASE=1 USE_XFSM=1 USE_JIT=0 USE_DEBUGGER=0 \
  USE_TAB_COMPLETE=0 USE_NETWORK_JS=0 PAD_FOR_BOOTLOADER=1 \
  SETDEFINES=<(printf '%s\n' 'DEFINES += -DNO_VECTOR_FONT=1') -j2
```

This option prefixes 65,536 bytes of `0xFF`, so the application begins at file
offset `0x10000`. It does not include or replace the board's bootloader. Do not
give the unpadded application-only BIN to **Flash from file**.

For the qualified 316,984-byte application, this clean build produced a
382,520-byte padded BIN. The prefix was entirely `0xFF`, the payload exactly
matched the qualified application, and the SHA-256 was
`e3415bee1b806090ba48cff088c8b9bef807a9ba3df7b5b7e7ed553fc58524b7`.
The Make rule retains the original application as the adjacent `.bin.unpadded`
file.

The Pico bootloader requires manual button handling. Follow Espruino's
[firmware-update procedure](https://www.espruino.com/Firmware+Update), put the
board into its pulsing serial-bootloader state, and confirm that its USB port
is free. The verified application address is `0x08010000`; do not write the
application binary at `0x08000000`, because that is the full-device base.

The 2026-10-27 qualification used Espruino's `scripts/stm32loader.py` with a
temporary Python 3 compatibility adaptation. The adaptation wrapped pyserial
so writes encode and reads decode Latin-1, materialized the two `map` results
as lists, tested the ELF prefix as bytes, and returned binary input with
`list(bytes)`. It then used:

```bash
python3 /tmp/xfsm-stm32loader3.py \
  -b 460800 -a 0x08010000 -e -w -v -X -k \
  -p /dev/ttyACM0 bin/espruino_2v29.537_pico_1r3.bin
```

Require the final `Verification OK` and successful reset. The loader performs
a mass erase, so this is not a way to preserve saved application data. The
temporary adapted loader is not stored in this repository; review and retain a
maintained Python 3 solution before making this a public flashing command.

On this run, the Web IDE advanced **Flash from file** operation reported
success for two unpadded application-only binaries but left the board without
its normal serial port and with a solid red LED. This was an artifact-selection
error, not evidence that either application image was invalid. A success prompt
alone is not readback verification; use the verified serial-loader route to
recover when that symptom occurs.

As a control after qualification, **Flash from URL** successfully loaded the
official `espruino_2v29_pico_1r3.bin` from `espruino.com`; it booted as
`PICO_R1_3`, version `2v29`, commit `6106910b8`. The official image contains
its bootloader region and application at their absolute file offsets. This
proves the Web IDE, bootloader, USB connection, and URL route were operational.
Physical verification of the `PAD_FOR_BOOTLOADER=1` local XFSM artifact is the
remaining file-flash check.

After flashing and reset, wait for the normal USB serial port. A successful
application boot does not leave the red LED continuously on. Run tests at
115,200 baud:

```bash
python3 tools/repl/run_test.py xfsm/tests/test_shell.js \
  --port /dev/serial/by-id/DEVICE --baud 115200 --timeout 30 --show-raw
```

The current detailed result is in the [Pico standalone qualification
report](reports/2026-10-27-pico-standalone-qualification.md).

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

The detailed historical measurements remain in the earlier
[Pico](reports/2026-09-29-m8-pico-physical-qualification.md) and earlier
[MDBT42Q](reports/2026-09-29-m8-mdbt42q-physical-qualification.md) reports.
The current Profile 2 procedures and results are in the
[Pico](reports/2026-10-27-pico-standalone-qualification.md) and
[MDBT42Q](reports/2026-10-26-mdbt42q-standalone-qualification.md) standalone
qualification reports.
