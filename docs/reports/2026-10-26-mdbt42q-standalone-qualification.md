# MDBT42Q Standalone Qualification

## Purpose

This report records physical qualification of the current standalone XFSM
Profile 2 candidate on an MDBT42Q. It covers the constrained Bluetooth build,
production JavaScript suites, canonical compatibility traces, and the
whole-interpreter save, reboot, restore, and reset lifecycle.

## Revisions And Target

| Item | Value |
| --- | --- |
| Board | `MDBT42Q` |
| Processor | Nordic nRF52832, ARM Cortex-M4F |
| Console | FTDI UART at 9,600 baud; board D6 TX and D8 RX |
| Espruino runtime | `2v29.537` |
| Espruino integration revision | `47c8a155df285e0264373c6578646f80981b8ae3` |
| Exported standalone source | `b2ae6b4c85ef8f4e2053d9639c36dc09064ac4c2` |
| Qualification tools | `008de0bc2c42765e28f5a527247de057fd699eb3` |
| Official Espruino upstream base | `3b5c8d97fa0678ec1da49a322f5f1fa990374a7a` |
| Specification | Public Profile 2 version 1.0, incorporating Profile 1 version 0.52 |
| Toolchain | ARM GCC 13.2.1 from `scripts/provision.sh MDBT42Q` |

## Build And Flash

The provisioned clean build used the constrained Bluetooth profile documented
in [Building Espruino XFSM](../building.md):

```bash
source scripts/provision.sh MDBT42Q
unset DEBUG
make BOARD=MDBT42Q clean
make BOARD=MDBT42Q RELEASE=1 DFU_UPDATE_BUILD=1 USE_XFSM=1 \
  USE_JIT=0 USE_DEBUGGER=0 USE_TAB_COMPLETE=0 USE_NETWORK_JS=0 USE_NFC=0 \
  SETDEFINES=<(printf '%s\n' 'DEFINES += -DNO_VECTOR_FONT=1') -j2
```

The image reports 312,728 code bytes and leaves 2,512 bytes before reserved
Storage at `0x6c000`. The DFU ZIP SHA-256 is
`d90104b0a49a2867b353f9f1515a0687d3a9559ee62e447d280bedc083458d18`;
the ELF SHA-256 is
`3edb3d9d842ded983bac63b206eead96501eb95f88d1ea173bb25fd04ec36f46`.
The remaining margin is still a release constraint and must be rechecked after
XFSM or upstream Espruino growth.

The DFU ZIP was flashed through the Web IDE Bluetooth bootloader. The running
board then reported `MDBT42Q`, `2v29.537`, integration commit `47c8a155d`,
SoftDevice 145, and the `XFSM` module. A Web IDE disconnect left the BlueZ
connection open; `bluetoothctl disconnect` was required before the firmware
returned its console to the FTDI UART.

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

Large traces were loaded through a temporary Storage string and erased after
execution. The lifecycle run saved and restored the interpreter image, then
confirmed that reset did not replay exit actions and removed the saved image.
The canonical trace run directly covers `XFC-CF-API-002`,
`XFC-CF-CONFIG-004`, `XFC-CF-CONFIG-005`, `XFC-CF-ACTION-002`,
`XFC-CF-SNAP-002`, `XFC-CF-TRANS-005`, `XFC-CF-DIAG-006`, and
`XFC-CF-COMPAT-006`. The established `Symbol` and property-enumerability
inputs remain reasoned skips because Espruino does not represent those inputs.

The machine-readable records are:

- [production suites and traces](../../tests/results/mdbt42q/2026-10-26-standalone-production-traces.json);
- [lifecycle](../../tests/results/mdbt42q/2026-10-26-standalone-lifecycle.json); and
- [qualification summary](../../tests/results/mdbt42q/2026-10-26-standalone-qualification.json).

## Runner Findings

The first pass exposed two low-speed serial-runner defects, not native engine
defects. At 9,600 baud the direct uploader needed a pause after every source
line to prevent `FIFO_FULL`. The completion detector also mistook echoed source
containing `DONE=` and a partially received `DONE=P` for completed output. It
now accepts only a complete `DONE=PASS` or `DONE=FAIL` line.

After those corrections, one unified rerun passed all 38 production and trace
entries, and the separate lifecycle rerun passed. No XFSM implementation or
firmware change was required.

## Decision

The current MDBT42Q constrained Bluetooth candidate advances from Profile 2
**Build verified** to **Conformance verified**. The current-candidate physical
repetition remains outstanding only for the Espruino Pico.
