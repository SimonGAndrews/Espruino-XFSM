# ESP32 Service-Coexistence Qualification

## Purpose

This report records the current standalone XFSM service-coexistence rerun on
an original ESP32 and an ESP32-C3. Each board was tested as the XFSM, BLE GATT
peripheral, WiFi station, and HTTPS/TLS client while the other board maintained
the GATT central connection.

## Revisions And Bench

| Item | Value |
| --- | --- |
| Standalone runner source | `eaa0e01d3c4e06c2d9dd431aa70fe938af0bea96` |
| Original ESP32 firmware | `ESP32_IDF5`, Espruino `2v29.536`, integration `0cab2c6755e2959672209c11ac5b1d60c46cd1e0` |
| Original ESP32 exported source | `74987aeaa1f700bfd5b79aaf35defea171918905` |
| ESP32-C3 firmware | `ESP32C3_IDF5`, Espruino `2v29.535`, integration `215fe4e16` |
| ESP32-C3 exported source | `563a3a0a36fc83aab84515481f516dc5738cca9b` |
| Official Espruino upstream base | `3b5c8d97fa0678ec1da49a322f5f1fa990374a7a` |
| Specification | Public Profile 2 version 1.0, incorporating Profile 1 version 0.52 |
| Network | Private `192.168.50.0/24` 2.4 GHz WiFi network |
| TLS endpoint | Host OpenSSL 3.0.13, TLS 1.2 |
| Relevant cases | `XFC-CF-RESOURCE-002`, `XFC-CF-HOST-001`, `XFC-CF-HOST-006` |

Both boards used their stock full-feature 70 KB native-heap profiles. Local
WiFi credentials and exact device addresses are excluded from retained
evidence.

## Method

The project-owned runner was executed twice in each direction. The larger
target role was written to temporary Espruino Storage, checked for exact length
and CRC, evaluated, and erased during cleanup.

```bash
python3 tools/repl/run_service_coexistence.py \
  --config tests/device/esp32-service/bench-config.local.json \
  --credentials tests/device/esp32-service/credentials.local.json \
  --direction c3-target --target-script-storage \
  --local-server-address 192.168.50.105 --timeout 90

python3 tools/repl/run_service_coexistence.py \
  --config tests/device/esp32-service/bench-config.local.json \
  --credentials tests/device/esp32-service/credentials.local.json \
  --direction classic-target --target-script-storage \
  --local-server-address 192.168.50.105 --timeout 90
```

Each successful run verified:

- firmware identity before the workload;
- BLE advertising, connection, service discovery, and GATT read/write;
- WiFi association and one correlated TLS 1.2 HTTPS request;
- the same BLE connection and another GATT write after HTTPS;
- an XFSM depth-24 service actor with a 49-action transition, five events,
  seven publications, and the expected ordered trace; and
- radio, WiFi, timer, Storage, and serial cleanup.

## Result

All four service runs passed: two with the C3 as target and two with the
original ESP32 as target. Every target reported 11 checks passed and zero
failed; every peer reported seven checks passed and zero failed. Each host
endpoint observed exactly one request and each XFSM actor ended in `Complete`.

| Target | Runs | Actor-ready JsVars used/free | Maximum runtime JsVars used | Minimum native heap | Native heap after cleanup |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original ESP32 | 2 pass | 1,422 / 1,436 | 1,079 | 22,672 bytes | 59,360 bytes |
| ESP32-C3 | 2 pass | 1,523 / 2,572 | 1,118 | 48,384 bytes | 66,428 bytes |

The table uses the lowest observed heap and final successful-run cleanup
values. Both targets retained useful JsVar and native-heap margin throughout
the combined workload.

The [machine-readable result](../../tests/results/esp32-service/2026-10-26-standalone-service-coexistence.json)
records the four run identifiers, resource observations, fixture hashes, and
firmware identities without credentials.

## Harness Finding

Two additional attempts stopped before advertising or service execution. One
detected a final Storage CRC mismatch; the other did not reliably recognize
the first write response. These were serial upload failures, not XFSM or
combined-service failures.

The runner now uses the shared XON/XOFF-aware serial connection, 192-byte
source chunks, explicit labeled write results, final length and CRC checks,
and one complete retry. The exact final runner content passed both target
directions without using that retry. No native XFSM or firmware change was
required.

## Decision

The current original ESP32 and ESP32-C3 candidates pass the combined
XFSM/BLE/WiFi/TLS service gate on the stock 70 KB native-heap profiles. This
closes the current-candidate two-board repetition; it does not replace the
portable, trace, lifecycle, or constrained-board qualification domains.
