# XFSM Tutorials

## Purpose

This directory is the canonical home for XFSM tutorial prose. Tutorials should
help an Espruino user build and understand a working application while linking
to the exact XFSM behaviour and reusable code on which they depend.

Place reusable executable JavaScript under [`examples/`](../../examples/) and
link to it from the tutorial. Do not maintain a second, gradually diverging
copy of the same application inside a tutorial.

## Authoring

- Write for an experienced hobbyist who understands JavaScript and basic
  microcontroller use but may be new to statecharts.
- Begin with the application and hardware outcome, then introduce only the XFSM
  concepts needed for each step.
- Identify the required board, firmware profile, connections, modules, and
  stored files before they are used.
- Use directly executable Espruino syntax and commands. Mark host-side or
  transpiled code clearly when it is unavoidable.
- Link supported behaviour to the current Profile 2 specification rather than
  treating complete XState or Stately behaviour as available in XFSM.
- Record how the complete tutorial and its linked example were tested.
- Keep diagrams readable on a light documentation page and retain editable
  project-authored source or layout metadata when practical.

## EspruinoDocs

Tutorials remain MPL-2.0 in this repository. Reusable files under `examples/`
remain MIT licensed. Before submitting selected material to EspruinoDocs,
follow the additional-licensing process in
[`CONTRIBUTING.md`](../../CONTRIBUTING.md) and recheck the current
[EspruinoDocs licence](https://github.com/espruino/EspruinoDocs/blob/master/LICENSE).

Prepare the EspruinoDocs version as an upstream adaptation. Apply its current
page metadata, tutorial location, image placement, and site-link conventions
without making the canonical XFSM tutorial depend on the EspruinoDocs build
system. The current upstream guidance is available in the
[EspruinoDocs repository](https://github.com/espruino/EspruinoDocs) and its
[Writing Tutorials guide](https://www.espruino.com/Writing+Tutorials).

Record the XFSM tutorial revision and linked example revision in the upstream
pull request so later changes can be reconciled deliberately.
