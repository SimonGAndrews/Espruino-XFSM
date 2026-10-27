# Espruino XFSM

XFSM is a compact native C state-machine engine for
[Espruino](https://www.espruino.com/). It exposes the `XFSM` JavaScript module
and implements a documented, resource-conscious compatibility profile informed
by [XState](https://github.com/statelyai/xstate).

XFSM is an independent implementation. It is not affiliated with or endorsed
by Espruino, Stately, or the XState maintainers.

## Names

| Use | Name |
| --- | --- |
| Standalone repository | `Espruino-XFSM` |
| Project, implementation, and specification | `Xstate-fsm-c` |
| Espruino module and build-library identifier | `XFSM` |
| Build variable | `USE_XFSM` |
| Internal C, native-format, diagnostic, and conformance prefix | `XFC` |

Application code normally sees only the public `XFSM` name through
`require("XFSM")`.

## Status

Profile 2 is the current public profile. It retains the completed Profile 1
contract and adds qualified shallow and deep history states. Native Format
Version 2 is frozen.

The implementation is Profile 2 Conformance verified on Linux Espruino and all
four specified physical target profiles: original ESP32 IDF5, ESP32-C3 IDF5,
the reduced Espruino Pico, and the constrained Bluetooth MDBT42Q.

See the [implementation status](docs/implementation-status.md) for the exact
qualified revisions, target status, and remaining work.

## Public Contract

- [Profile 2 specification](docs/specification-profile-2.md) - current
  normative entry point
- [Profile 1 specification](docs/specification.md) - frozen Profile 1 base
- [History-state requirements](docs/extensions/history-states.md) - normative
  Profile 2 extension
- [Native Format Version 2](docs/native-format-v2.md) - frozen private Profile
  2 arena and actor layout
- [Conformance record](tests/profile-2-conformance.md) - requirements and
  supporting evidence

The specifications govern supported behaviour. XState executions, Stately
exports, SCXML, and older project material are compatibility evidence unless a
specification explicitly adopts them.

## Repository Layout

- [`xfsm/`](xfsm/) - canonical deployable library tree; maps unchanged to
  `libs/xfsm/` in an Espruino checkout
- [`docs/`](docs/) - specifications, architecture, build guidance, and reviewed
  reports
- [`tests/`](tests/) - conformance definitions, differential runners, and
  recorded results
- [`examples/`](examples/) - reusable MIT-licensed application examples
- [`tools/`](tools/) - canonical export, verification, and physical-test
  tooling

The [build guide](docs/building.md) explains how to place the library in an
Espruino checkout and build firmware with `USE_XFSM=1`.

## Development

- [Contributing](CONTRIBUTING.md) defines the contract, licensing, provenance,
  and source-notice rules.
- [Espruino integration](docs/espruino-integration.md) explains how committed
  library source is exported and tested in an Espruino checkout.
- [Building](docs/building.md) records verified host and target commands.
- [Physical device testing](docs/device-testing.md) records flashing, serial,
  recovery, and evidence procedures for the supported target families.
- [Tests](tests/README.md) explains conformance, differential references, and
  recorded evidence.
- [Examples](examples/README.md) defines reusable application-example rules.
- [Tutorials](docs/tutorials/README.md) defines the local authoring and
  EspruinoDocs contribution workflow.

## Licensing

MPL-2.0 is the repository default. Files under `examples/` are provided under
the MIT License so applications and tutorials can reuse them easily. See
[LICENSING.md](LICENSING.md) for the precise boundary and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for upstream provenance.

## Commercial Use And Upstream Support

XFSM is open-source software and may be used commercially under its applicable
licences. XFSM runs within Espruino and is informed by the state-machine model
established by XState.

Organizations benefiting from XFSM are encouraged to support the upstream
projects directly through [Espruino's support
channels](https://www.espruino.com/Donate) and the [XState Open
Collective](https://opencollective.com/xstate), as well as through code,
testing, and documentation contributions.

This request is voluntary and does not add to or modify the applicable licence
obligations.
