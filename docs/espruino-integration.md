# Espruino Integration Workflow

This guide explains how an XFSM change moves from this repository into an
Espruino build for testing and, when it is ready, an upstream contribution.

## How This Repository Is Used

This repository is where XFSM is developed and maintained. It contains the
XFSM library, specifications, tests, test results, examples, tools, and
supporting documentation.

The [`xfsm/`](../xfsm/) directory contains the files that are copied into
Espruino's `libs/xfsm/` directory when XFSM is tested or built as part of
Espruino. The two directories must contain the same files.

The Espruino repository provides the interpreter, build system, board
definitions, and release process into which XFSM is integrated. Changes to
those parts are developed and reviewed in the Espruino repository.

## Development Workflow

In summary, XFSM changes are made and committed in this repository. The export
tool then copies the committed XFSM library into a separate Espruino source
repository. The standard Espruino build system is used there to build XFSM into
the Linux version of Espruino or into firmware for a supported board. The Linux
version can run automated tests, while the firmware can be flashed to a board
for target testing.

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

The export tool requires Git, `tar`, and `rsync`. Both repositories must have
clean working trees before it will run.

From the root of this repository, run:

```bash
./tools/export-to-espruino.sh /path/to/Espruino
```

The tool copies the committed contents of `xfsm/`, not uncommitted or ignored
files from the working directory. It makes `libs/xfsm/` an exact copy, so it
also removes any extra files under that directory. Files elsewhere in the
Espruino checkout are not changed.

Some tests create temporary files under `libs/xfsm/`, such as
`tests/native/build/` and `tests/__pycache__/`. These files are not part of the
XFSM source. The export command removes them, while `--check` reports that the
directories differ if they are present. Run `--check` after committing the
export and before running the tests, or remove the temporary files first.

The tool prints the exact commands needed to enter the Espruino repository,
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

The export command checks the copied files before it succeeds. The `--check`
option is also available when the two directories need to be compared later
without changing either of them:

```bash
./tools/export-to-espruino.sh --check /path/to/Espruino
```

Run this command from the `Espruino-XFSM` repository before building or after
removing generated files from `libs/xfsm/`. It succeeds only when both
repositories are clean and the two library directories match.

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
The current branches and integration status are recorded in
[Implementation Status](implementation-status.md).

## Contributing To Espruino

An Espruino pull request should contain `libs/xfsm/` and the smallest Espruino
build changes needed to select the library. XFSM specifications, development
records, and project documents stay in this repository and can be linked from
the pull request.

CI changes used only to test the development fork do not need to be included
in the upstream pull request.

Tutorials and examples can be maintained here and proposed separately to
EspruinoDocs under that repository's documentation and example licences.

## Earlier XFSM Commits

The XFSM commit history before this repository was created was extracted from
`libs/xfsm/` on the `feature/xfsm-profile2` branch of
`SimonGAndrews/Espruino`. The extraction preserved the changes, authors,
dates, and messages, but produced new commit identifiers. Older test results
therefore continue to name their original Espruino commits.
