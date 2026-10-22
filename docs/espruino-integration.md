# Espruino Integration Workflow

## Ownership Boundary

This repository is the canonical source for the XFSM library, specifications,
tests, and evidence. The [`xfsm/`](../xfsm/) directory is the deployable library
tree and maps unchanged to `libs/xfsm/` in an Espruino checkout.

The Espruino repository remains authoritative for its build system, board
definitions, interpreter APIs, and release process. XFSM does not vendor the
whole Espruino tree.

## Development Flow

1. Make and review library-local changes under `xfsm/` in this repository.
2. Commit the reviewed changes so the canonical checkout is clean.
3. Export that commit to `libs/xfsm/` in a clean Espruino feature branch with
   `tools/export-to-espruino.sh`.
4. Inspect the Espruino diff and commit the mirror with the reported
   `XFSM-Source: <commit>` trailer.
5. Keep any required Espruino Makefile, CI, or board-file changes as separate
   commits in that feature branch.
6. Build and test through Espruino using the commands in
   [building.md](building.md).
7. Record both the XFSM commit and Espruino commit in new result evidence.

For a local export where both repositories are clean:

```bash
/path/to/Espruino-XFSM/tools/export-to-espruino.sh \
  /path/to/Espruino
```

The exporter rejects dirty source and destination repositories. It builds the
mirror from the committed `xfsm/` tree rather than the working directory, so
ignored build products and other untracked files cannot enter the integration
commit. Deletion is limited to `libs/xfsm/`, and the resulting tree is verified
before the command succeeds.

After committing the exported tree in Espruino, verify the clean mirror without
changing it:

```bash
/path/to/Espruino-XFSM/tools/export-to-espruino.sh --check \
  /path/to/Espruino
```

`--check` also requires both repositories to be clean and reports the exact
canonical commit being compared.

`libs/xfsm/` is a deployment mirror, not a second development location. If
integration or upstream review reveals a required library change, apply and
commit it in this repository, then export it again. Espruino Makefile, CI,
board, and release changes remain native Espruino work and are not copied back
into XFSM.

## Upstream Contribution Shape

An Espruino pull request should contain the deployable `libs/xfsm/` tree and the
small host-build changes needed to select it with `USE_XFSM=1`. Standalone
specifications, historical measurements, and project-governance files remain
in this repository and should be linked rather than copied into Espruino.

The current integration branch has three host-side changes outside
`libs/xfsm/`:

- `Makefile` conditionally adds the wrapper, engine sources, include path, and
  measurement or fault-injection sources when their build flags are selected;
- `.github/workflows/xfsm.yml` provides dedicated fork CI; and
- `.github/workflows/build.yml` allows the fork workflow to run on branch names
  containing `/`.

Only the Makefile selection is required by the library. The workflow changes
are development support and may be omitted from an upstream pull request.

User tutorials may be maintained here and proposed separately to
EspruinoDocs under that repository's documentation and example licences.

## Migrated History

The standalone Git history through the initial import was extracted from
`libs/xfsm/` on `SimonGAndrews/Espruino` branch `feature/xfsm-profile2`.
Extraction rewrote commit identifiers while preserving the XFSM changes,
authors, dates, and messages. Historical reports and JSON records intentionally
retain the original Espruino commit identifiers.
