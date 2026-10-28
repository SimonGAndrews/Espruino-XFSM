# Test Results

This directory is the authoritative evidence location for every test performed
for the Wi-Fi greenhouse soil-heater example. Do not retain the only copy of a
result in terminal scrollback, an external notes file, or a repository-level
report directory.

Results are grouped first by experiment and then by an immutable run ID:

```text
test-results/
  wifi-event-characterisation/
    YYYY-MM-DDTHHMMSSZ-test-a-short-label/
      metadata.md
      raw-serial.log
      operator-notes.md
      findings.md
```

Use UTC in the run ID so filenames remain unambiguous. Use one directory for
each independent run and never overwrite an earlier run when repeating a test.
Use lower-case test letters (`test-a` through `test-f`). A test with multiple
deliberately separate phases may store additional raw files in the same run
directory when their relationship is explained in `metadata.md`.

## Required Files

- `metadata.md` records the scenario, revisions, hardware, configuration role,
  timing parameters, operator steps, and result disposition. Copy
  [`run-metadata.template.md`](run-metadata.template.md) when starting a run.
- `raw-serial.log` is the complete, unedited console capture, including
  `WIFI_DIAG` records and any interpreter output. Redact secrets only in a
  derived publication copy; preserve the fact and method of any redaction in
  the metadata.
- `operator-notes.md` records wall-clock times for physical operations,
  unexpected observations, interruptions, and deviations from the procedure.
- `findings.md` contains reviewed observations and conclusions. Keep facts
  distinct from interpretations and do not invent missing event ordering.

The executable diagnostic is not duplicated into each run. The canonical
source is
[`../wifi-event-characterisation.js`](../wifi-event-characterisation.js).
Every run's metadata records that path and the SHA-256 of the exact source that
was loaded. Git history provides the source reconstruction after the diagnostic
is committed; pre-commit runs also state their working-tree limitation.

Never store passwords, credential configuration files, or authentication
tokens in this directory. Review every capture for secrets before adding it to
Git. Connected SSIDs may be intentionally redacted by the diagnostic and must
not be reconstructed in retained output.

Later test families should receive their own subdirectory under
`test-results/` and follow the same immutable-run principle.
