# ESP32 Service-Coexistence Testing

## Purpose

This procedure checks that XFSM can operate on an ESP32 while BLE GATT, WiFi,
and HTTPS/TLS are active together. It uses an original ESP32 and an ESP32-C3 so
either board can be the target while the other acts as the GATT peer.

The focused runner and fixtures are maintained in this repository. The earlier
ESP32 bench repository is not required.

The workload previously passed four physical runs. Its repository-local move
has passed syntax, configuration, and path checks; repeat it on both connected
boards before treating the relocated runner itself as fresh physical evidence.

## Requirements

- one original ESP32 with an `ESP32_IDF5` XFSM build;
- one ESP32-C3 with an `ESP32C3_IDF5` XFSM build;
- distinct persistent serial paths for both boards;
- a 2.4 GHz WiFi network reachable by the selected target;
- Python 3, `pyserial`, and `openssl`; and
- a host IPv4 address reachable from that WiFi network.

Flash and identify both boards using their device guides before configuring
the bench. The runner refuses to start the workload when the observed board,
Espruino version, or Git revision differs from the configured identity.

## Local Configuration

Create the two ignored local files from the committed templates:

```bash
cp tests/device/esp32-service/bench-config.example.json \
  tests/device/esp32-service/bench-config.local.json
cp tests/device/esp32-service/credentials.example.json \
  tests/device/esp32-service/credentials.local.json
chmod 600 tests/device/esp32-service/credentials.local.json
```

In `bench-config.local.json`, replace both USB paths and all expected firmware
values with the identities observed on the two attached boards. Persistent
`/dev/serial/by-id` or `/dev/serial/by-path` names are preferred. In
`credentials.local.json`, enter the local SSID and password. These files are
ignored by Git and must never be added to an evidence transcript.

Confirm that the host address is on the same network as the target:

```bash
ip -4 address
```

## Run The Workload

Release both serial ports, then run from the standalone repository:

```bash
python3 tools/repl/run_service_coexistence.py \
  --config tests/device/esp32-service/bench-config.local.json \
  --credentials tests/device/esp32-service/credentials.local.json \
  --direction c3-target \
  --target-script-storage \
  --local-server-address HOST_IPV4 \
  --timeout 90
```

Use `--direction classic-target` to reverse the target and peer. The runner:

1. verifies both runtime identities;
2. reboots and resynchronizes both boards;
3. starts a temporary TLS 1.2 HTTPS endpoint with a generated certificate;
4. preloads the XFSM service actor on the target;
5. stores and evaluates the larger target role from flash when
   `--target-script-storage` is selected, using bounded writes and a final
   length and CRC check;
6. holds a GATT connection across WiFi association and the HTTPS request;
7. confirms another GATT write after HTTPS;
8. correlates both boards' structured results; and
9. disconnects radio services and erases the temporary target script.

The target role receives credentials while REPL echo is disabled. The runner
prints neither the SSID nor password. Review raw output before retaining it if
the run was interrupted during setup.

## Acceptance

A successful run ends with `RUNNER_RESULT=PASS`. It must also show one
successful target completion, one successful peer completion, the host HTTPS
request, and the ordered XFSM service trace. Run both directions when assessing
the two target families, and repeat the selected product direction enough to
exercise radio and TLS allocation more than once.

Record both firmware identities, direction, host address class rather than
network credentials, runner command, number of runs, structured results, and
cleanup status. The original four-run evidence and its resource interpretation
remain in the
[service-coexistence report](reports/2026-09-28-m7-esp32-c3-service-coexistence.md).
