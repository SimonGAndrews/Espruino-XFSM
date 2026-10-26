# Espruino Integration Workflow

This guide explains how an XFSM change moves from this repository into an
Espruino build for testing and, when it is ready, an upstream contribution.

## How This Repository Is Used

This repository is where XFSM is developed and maintained. It contains the
XFSM library, specifications, tests, test results, examples, tools, and
supporting documentation.

This repository is separate from the Espruino source repository. The Espruino
repository provides the interpreter source, build system, board definitions,
and release process into which XFSM is integrated.

This repository's [`xfsm/`](../xfsm/) directory contains the files that are
copied into Espruino's `libs/xfsm/` directory when XFSM is tested or built as
part of Espruino. The two directories must contain the same files.

## Development Workflow

In summary, XFSM changes are made and committed in this repository. An export
tool then copies the committed XFSM library into a separate Espruino source
repository. The standard Espruino build system is used there to build XFSM into
the Linux version of Espruino or into firmware for a supported board. The Linux
version can run automated tests, while the firmware can be flashed to a board
for target testing.

In detail:

1. Develop the XFSM library and its tests in this repository. Update the
   specification and other project documents when the change requires it.
2. Review and commit the change. Run any checks that do not require an Espruino
   build. The export tool only copies files from the current committed XFSM
   revision.
3. In a separate checkout of the Espruino source repository, create or select
   a clean feature branch for XFSM integration and testing.
4. Run `tools/export-to-espruino.sh` to copy `xfsm/` into the Espruino
   repository as `libs/xfsm/`.
5. Inspect and commit the exported files in the Espruino repository. In that
   commit message, add an `XFSM-Source: <commit>` reference line containing
   the full 40-character hash of the source commit from this `Espruino-XFSM`
   repository.
6. Make any required Espruino build, board, or CI changes as separate Espruino
   commits.
7. Build and test XFSM through Espruino using the commands in
   [Building Espruino XFSM](building.md).
8. Record important results in this repository, including both the XFSM and
   Espruino commit identifiers.

The exporter uses the checked-out XFSM commit, regardless of its branch. A
feature branch can therefore be exported for development testing. For a
release or an Espruino pull request, export a reviewed commit from `main`. If
another branch must be used, identify it in the release or pull-request notes.

## Exporting XFSM

The tool has two execution modes:

- **Export (default)** copies the committed `xfsm/` directory from this
  repository into the Espruino repository as `libs/xfsm/`. Use this mode when
  an XFSM change is ready to be built and tested with Espruino.
- **Check (`--check`)** compares the committed `xfsm/` directory with
  Espruino's `libs/xfsm/` directory without changing either repository. Use
  this mode to confirm that Espruino contains an exact copy of the currently
  checked-out XFSM commit.

Both modes require Git, `tar`, and `rsync`. Both repositories must also have
clean working trees.

### Export Mode

From the root of this repository, run:

```bash
./tools/export-to-espruino.sh /path/to/Espruino
```

The tool copies the committed contents of this repository's `xfsm/` directory,
not uncommitted or ignored files from the working directory. It makes
`libs/xfsm/` in the Espruino source repository an exact copy, so it also
removes any extra files under that directory. Files elsewhere in the Espruino
checkout are not changed.

The tool prints the exact commands needed to enter the Espruino source repository,
review the exported files, and commit them. The output has this form, with the
actual repository path and XFSM source hash filled in:

```bash
cd /path/to/Espruino
git add -A -- libs/xfsm
git diff --cached -- libs/xfsm
git commit \
  -m "Update XFSM library" \
  -m "XFSM-Source: <actual source hash>"
```

The export command checks the copied files before it succeeds.

### Check Mode

From the root of this repository, run:

```bash
./tools/export-to-espruino.sh --check /path/to/Espruino
```

Check mode does not copy, remove, stage, or commit any files. It succeeds only
when both repositories are clean and the two library directories match.

Note: Some tests create temporary files under `libs/xfsm/`, such as
`tests/native/build/` and `tests/__pycache__/`. These files are not part of the
XFSM source. Export mode removes them, while check mode reports that the
directories differ if they are present. Run check mode after committing the
export and before running the tests, or remove the temporary files first.

Do not edit `libs/xfsm/` as a separate copy of the library. If Espruino testing
finds a problem in XFSM, make and commit the correction here, then export it
again.

## Espruino-Side Changes

Espruino files outside `libs/xfsm/` remain part of the Espruino project. These
include:

- the Makefile support that selects XFSM with `USE_XFSM=1`;
- board definitions that choose whether to include XFSM;
- Espruino CI and test configuration; and
- Espruino release and packaging changes.

Keep these changes separate from the exported library commit. This makes it
clear which files came from XFSM and which changes adapt the Espruino build.

## Updating Project Status

[Implementation Status](implementation-status.md) is the project's living
summary of the current XFSM and Espruino integration branches and revisions,
completed qualifications, current work, and blockers. Update it when the active
branch changes, a revision becomes the current public or qualified version, a
milestone or qualification is completed, the next major development step
changes, or a new blocker affects the planned work. Routine exports and test
runs only need an update when they change that overall status; their detailed
results belong in the relevant test record or report.

## Contributing To Espruino
Changes to XFSM should be shared with espruino master https://github.com/espruino/Espruino via a pull request.

The pull request should contain `libs/xfsm/` and the smallest Espruino
build changes needed to select the library. XFSM specifications, development
records, and project documents stay in this repository and can be linked from
the pull request.

CI changes used only to test the development fork do not need to be included
in the upstream pull request.

Tutorials and examples can be maintained here and proposed separately to
EspruinoDocs under that repository's documentation and example licences.

## Earlier XFSM Commits

Early XFSM development took place in the Espruino repository. When that history
was copied into this standalone repository, Git assigned new commit hashes
because the surrounding repository history had changed. Older test reports
still identify the original commits in `SimonGAndrews/Espruino`; new results
record both the XFSM source commit and the corresponding Espruino integration
commit. Use the [XFSM Migrated Commit Map](migrated-commit-map.md) to find the
corresponding standalone commit for an older Espruino commit.
