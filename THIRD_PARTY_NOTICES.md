# Third-Party Notices

This document records third-party projects and materials relevant to XFSM. The
XFSM licences do not replace their respective licences.

## XState

XFSM implements an independently specified, limited compatibility profile
informed by XState behaviour, documentation, and differential tests.

- Project: XState
- Upstream: https://github.com/statelyai/xstate
- Licence: MIT
- Copyright notice: Copyright (c) 2015 David Khourshid
- Primary differential reference: XState 5.33.2
- Secondary differential reference: XState 4.38.3

No XState implementation source is incorporated into the XFSM engine. Any
example later copied or adapted from an MIT-licensed XState repository must
identify its exact source and preserve this copyright and permission notice:

> The MIT License (MIT)
>
> Copyright (c) 2015 David Khourshid
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to
> deal in the Software without restriction, including without limitation the
> rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
> sell copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

Material published only through Stately's website or an unlicensed repository
must not be assumed to carry XState's MIT licence. Link to it as a reference or
obtain permission rather than copying it.

## Espruino

XFSM is designed to be compiled as an optional native library within Espruino.

- Project: Espruino
- Upstream: https://github.com/espruino/Espruino
- Licence: Mozilla Public License 2.0

The `xfsm/` directory is XFSM's canonical deployable library tree. It uses
Espruino's public native-library integration interfaces but does not include a
copy of the wider Espruino source tree. Files copied into or modifications made
directly to Espruino remain subject to their applicable notices. A distribution
combining XFSM with Espruino must comply with MPL-2.0 for all covered files.

## Stately Exports

The fixtures under `docs/compatibility/` and the layout metadata in the
project-authored thermostat example were exported by Stately tooling from
project-authored machine models. Fixture source, tool profile, and adaptations
are recorded in `docs/compatibility/register.json`. They do not copy Stately
documentation or implementation source.

## Standards And Tools

The W3C SCXML Recommendation and Stately tooling are compatibility and design
references. Their identification here does not assert that their source code
or documentation is included in XFSM.

XFSM is an independent project. References to XState, Stately, and Espruino are
descriptive and do not imply affiliation with or endorsement by their
maintainers.
