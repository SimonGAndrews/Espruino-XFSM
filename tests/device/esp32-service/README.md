# ESP32 Service-Coexistence Fixtures

This directory contains the peer JavaScript role and local configuration
templates used by the XFSM BLE, WiFi, and HTTPS service-coexistence runner.

- `ble_gatt_hold_client.js` keeps the peer GATT connection active before and
  after the HTTPS request.
- `bench-config.example.json` describes both USB positions and the exact
  firmware identity expected at each position.
- `credentials.example.json` documents the local credential shape without
  containing a real password.

Local `bench-config.local.json` and `credentials.local.json` files are ignored
by Git. See
[`docs/service-coexistence-testing.md`](../../../docs/service-coexistence-testing.md)
for the complete procedure.
