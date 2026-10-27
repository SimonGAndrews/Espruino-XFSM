# Espruino Pico Standalone Qualification

## Purpose

This report records physical qualification of the current standalone XFSM
Profile 2 candidate on an Espruino Pico. It covers the reduced Pico build,
production JavaScript suites, canonical compatibility traces, and the
whole-interpreter save, reboot, restore, and reset lifecycle.

## Revisions And Target

| Item | Value |
| --- | --- |
| Board | `PICO_R1_3` |
| Processor | STM32F401CDU6, ARM Cortex-M4F |
| Console | USB serial at 115,200 baud |
| Espruino runtime | `2v29.537` |
| Espruino integration revision | `47c8a155df285e0264373c6578646f80981b8ae3` |
| Exported standalone source | `b2ae6b4c85ef8f4e2053d9639c36dc09064ac4c2` |
| Clean evidence checkout | `017ec1cd5f5cb0a018c3a60c0affdf4f2f8ec9b3` |
| Qualification tools | `008de0bc2c42765e28f5a527247de057fd699eb3` |
| Official Espruino upstream base | `3b5c8d97fa0678ec1da49a322f5f1fa990374a7a` |
| Specification | Public Profile 2 version 1.0, incorporating Profile 1 version 0.52 |
| Toolchain | ARM GCC 13.2.1 from `scripts/provision.sh PICO_R1_3` |

## Build And Flash

The provisioned clean build used the reduced Pico profile documented in
[Building Espruino XFSM](../building.md):

```bash
source scripts/provision.sh PICO_R1_3
unset DEBUG
make BOARD=PICO_R1_3 clean
make BOARD=PICO_R1_3 RELEASE=1 USE_XFSM=1 USE_JIT=0 USE_DEBUGGER=0 \
  USE_TAB_COMPLETE=0 USE_NETWORK_JS=0 \
  SETDEFINES=<(printf '%s\n' 'DEFINES += -DNO_VECTOR_FONT=1') -j2
```

The application binary is 316,984 bytes and leaves 10,696 bytes below the
327,680-byte application limit. Its SHA-256 is
`2420a2f6ba57db802e6fe868c352b1dcfc571eb65138d1a6bdd0c4e0c04b4e9b`;
the ELF SHA-256 is
`eaf0d21ddd1e041904041800f0a0fc5040efb6948c805e52cc27f7b9b39aa5ba`.

The 316,984-byte build product is an application-only image whose byte zero is
intended for flash address `0x08010000`. The Web IDE advanced **Flash from
file** operation reported success when given that file directly but left the
board without a normal serial port and with its red LED continuously on.
Repeating the same mistake with the previously qualified application-only
`2v29.450` image had the same result.

The board was recovered through its serial bootloader using Espruino's
`scripts/stm32loader.py` with the small Python 3 compatibility adaptation
described in [Constrained ARM Device Testing](../constrained-arm-device-testing.md).
The loader mass-erased the application area, wrote at `0x08010000`, read every
byte back, reported `Verification OK`, and reset the board. The known-good
image first booted and reported its expected identity. The same verified route
then loaded the current image, which booted without the solid red LED and
reported `PICO_R1_3`, `2v29.537`, integration commit `47c8a155d`, and the
`XFSM` module.

After qualification, the Web IDE **Flash from URL** operation successfully
loaded the official
`https://www.espruino.com/binaries/espruino_2v29_pico_1r3.bin`. The board then
booted normally and reported `PICO_R1_3`, version `2v29`, and commit
`6106910b8`. That 390,232-byte distribution image contains a bootloader region
in its first 65,536 bytes and places its application at file offset `0x10000`.
This control shows that the Web IDE, USB connection, bootloader, and URL
flashing path work.

Espruino's Makefile explains the failed local-file attempts: a Pico BIN for the
Web IDE must be built with `PAD_FOR_BOOTLOADER=1`. This preserves the absolute
file position by prefixing 65,536 bytes of `0xFF`; it does not add another
bootloader. A clean Make build with that option produced a 382,520-byte
candidate with SHA-256
`e3415bee1b806090ba48cff088c8b9bef807a9ba3df7b5b7e7ed553fc58524b7`.
Its prefix is entirely `0xFF` and its remaining bytes exactly match the
qualified application. Physical **Flash from file** verification of that
padded artifact remains to be performed.

The qualified `2v29.537` XFSM image was then restored through the verified
serial-loader route. Full readback again reported `Verification OK`; after
reset, `test_shell.js` passed and confirmed `PICO_R1_3`, `2v29.537`, and
integration commit `47c8a155d`. The board was left running this XFSM image.

## Physical Result

All current production checks passed:

- 29 of 29 production JavaScript suites;
- nine of nine canonical traces, compared exactly with their reviewed output;
- shallow and deep history semantics and diagnostics;
- direct and Storage-backed depth-32 execution, including the 65-action
  transition;
- host callbacks, GC cleanup, event serialization, allocation pressure, and
  diagnostic pressure; and
- save, reboot, restoration without replay, `reset(true)`, and saved-image
  cleanup.

The depth-32 transition test used 1,139 of 5,100 JsVar blocks at its measured
transition point. The eight-actor cleanup test retained 2,638 free blocks while
the live graph was present and returned exactly to its settled baseline. The
Storage-backed depth test returned from 1,106 compiled-use blocks to 324 after
cleanup.

The lifecycle run saved and restored the interpreter image through flash
compaction, then confirmed that reset did not replay exit actions and removed
the saved image. The canonical trace run directly covers `XFC-CF-API-002`,
`XFC-CF-CONFIG-004`, `XFC-CF-CONFIG-005`, `XFC-CF-ACTION-002`,
`XFC-CF-SNAP-002`, `XFC-CF-TRANS-005`, `XFC-CF-DIAG-006`, and
`XFC-CF-COMPAT-006`. The established `Symbol` and property-enumerability
inputs remain reasoned skips because Espruino does not represent those inputs.

The production and lifecycle runners were invoked from the clean standalone
checkout with:

```bash
python3 tools/repl/run_qualification_suite.py pico-reduced \
  --port /dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_00000000001A-if00 \
  --baud 115200 --timeout 180 \
  --expected-version 2v29.537 --expected-git-commit 47c8a155d \
  --keep-going --output /tmp/xfsm-pico-final-qualification.json

python3 tools/repl/run_lifecycle_test.py \
  --port /dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_00000000001A-if00 \
  --baud 115200 --timeout 180 --expected-board PICO_R1_3 \
  --expected-version 2v29.537 --expected-git-commit 47c8a155d \
  --output /tmp/xfsm-pico-current-lifecycle.json
```

The machine-readable records are:

- [production suites and traces](../../tests/results/pico/2026-10-27-standalone-production-traces.json);
- [lifecycle](../../tests/results/pico/2026-10-27-standalone-lifecycle.json); and
- [qualification summary](../../tests/results/pico/2026-10-27-standalone-qualification.json).

## Decision

The current reduced Pico candidate advances from Profile 2 **Build verified**
to **Conformance verified**. All four specified physical target profiles now
pass the current Profile 2 qualification.
