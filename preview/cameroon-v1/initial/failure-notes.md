# Genuine failures and corrections
- Initial raw GLB theme assertion expected `Side_ring`, the sanitized runtime name. Raw exported node is `Side ring / mount`; corrected format-specific expectation, preserving required-feature assertion.
- Extended browser assertion expected one relief mesh directly parented to lid. Actual GLTFLoader correctly splits the two-material relief into two meshes beneath the named Fako group. Corrected to two mesh primitives, checked full ancestry and aggregate span. Raw failure retained. This is a harness correction, not repaired geometry.
- First browser command timed out at 180 seconds. Existing complete captures were not treated as a pass; reran with a larger bounded timeout.
- Optional Codex exited with HTTP 401/token refresh failure before implementation; no accepted changes, no credential access or edits. Hermes authored and tested directly.
