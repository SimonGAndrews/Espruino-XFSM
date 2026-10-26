# XState V4 Reference Environment

This package pins the Profile 1 migration reference to `xstate@4.38.3`. It is
compatibility evidence and test tooling, not runtime code for Espruino.

Install exactly the locked dependency tree and run the asserted reference:

```bash
npm ci --ignore-scripts
npm test
```

The runner checks the installed version and records the retained `cond` and
`internal` aliases, v4 ordered-action flags, and action-boundary behavior used
by XFSM compatibility cases.

Do not update the dependency version or regenerate `package-lock.json` without
reviewing the compatibility profile, expected trace, provenance register, and
corresponding XState v5 behavior.
