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
2. Copy the complete `xfsm/` tree to `libs/xfsm/` in a clean Espruino feature
   branch.
3. Keep any required Espruino Makefile, CI, or board-file changes as separate
   commits in that feature branch.
4. Build and test through Espruino using the commands in
   [building.md](building.md).
5. Record both the XFSM commit and Espruino commit in new result evidence.
6. Bring reviewed library changes back here before treating them as canonical.

For a local synchronization where both directories are clean and reviewed:

```bash
rsync -a --delete \
  /path/to/Espruino-XFSM/xfsm/ \
  /path/to/Espruino/libs/xfsm/
```

Always inspect `git diff` in the destination before committing. The `--delete`
option is intentional because the destination must represent the complete
canonical library tree, but it must not be used against an unreviewed or dirty
destination.

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
