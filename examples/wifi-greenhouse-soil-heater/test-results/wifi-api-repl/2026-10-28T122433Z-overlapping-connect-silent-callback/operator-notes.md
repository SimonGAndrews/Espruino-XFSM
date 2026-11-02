# Operator Notes

- The reproduction was run manually in the Espruino Web IDE REPL.
- No access point or other bench hardware was operated during this test.
- Exact start and end times were not captured by the diagnostic.
- The operator supplied the complete visible REPL transcript after the run.
- The Web IDE screenshot was retained at
  `images/WifiIssueRepl_twoConnects.png`. It shows the Espruino `2v29.535`
  banner, detected `ESP32C3_IDF5` profile, Web Serial identifier, complete
  reproduction code, and corresponding console output in a single frame.
- The canonical `.js` file was saved after the physical run and includes an
  MIT licence header not shown in the editor. Its hash therefore identifies a
  functionally matching retained reconstruction, not the exact uploaded bytes.
- The ESP-IDF log line appears before the JavaScript `starting connection 2`
  line in the captured console. Output from the ESP-IDF task and JavaScript
  console may be interleaved, so that display order is not treated as evidence
  that the driver error preceded the second call.
- This run is a minimal, manually reviewable reproduction of behaviour also
  seen in the instrumented Test F evidence. It does not exercise XFSM.
