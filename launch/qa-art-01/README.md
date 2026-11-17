# QA-ART-01 — independent review complete, launch holds retained

Parent `t_e669e48c`, exact commit `6f59f7c47540284a1470f8451db90b6d070d6171`, branch `feature/art-01-review`. Its remote SHA was read back. Read-only snapshot is under `launch/art-01/` within this evidence folder; no source preview or parent worktree was modified.

## Verdict
All 26 assigned IDs accounted for: **9 bounded candidate passes, 17 needs-user-review**. No art changes, new approval, critical reproducible failure, or permission to release. `reviewed-ledger.json` is the machine-readable handoff. Namibia's full archive-inventory hold remains unresolved despite passing selected-payload checks. All final-user approval, full acceptance, storage and mint/release holds remain.

Four isolated read-only visual inspectors individually loaded all 104 original desktop/mobile closed/open captures plus 26 matching marketing images, not merely comparison boards. Their per-image findings are retained in `visual-a.json` through `visual-d.json`. The lead additionally inspected Lesotho's original desktop and fresh mobile open view, Panama's comparison and Malaysia's comparison. Original images are preserved in the exact-byte parent snapshot.

## Fresh checks executed by QA
- `python launch/qa-art-01/verify.py`: all 276 inventoried parent evidence files match committed blobs and extracted files; all 26 selected viewers/source files/marketing files match immutable hashes and sizes. Delivered viewers equal committed bytes and all are strictly below 5,000,000 bytes. Every selected GLB is embedded verbatim in its HTML.
- All 26 ZIPs: exact archive hash/size, CRC, unique safe paths, and **exact selected HTML/GLB/BLEND member bytes**, stronger than basename presence alone. Full internal archive inventory was NOT rerun; Namibia hold retained.
- `python launch/qa-art-01/smoke_viewers.py --ids lesotho panama malaysia`: six offline Edge cases passed. Desktop 1440x1080 and emulated touch 390x844: load, drag, reset, open/close, interrupted reset, reduced-motion endpoints, no horizontal overflow, external requests or page errors. Viewer hash checked before opening.
- All other parent browser cases and all motion tests were inspected as committed evidence, NOT relabeled independent fresh execution. No changed art exists requiring a fresh changed-art acceptance suite.

## Findings and qualifications
Panama retains a visible three-tree marketing / two-tree model mismatch. Malaysia marketing is mauve with a dark inset while runtime is crimson with a warmer inset. These are art-direction holds, not authority to regenerate.

Parent prose is qualified in the independent ledger: Georgia and Guyana marketing also retain faceting/simplification; Slovakia's white ornaments visibly project; Turkey's supposedly richer glaze is not conclusively established; Zimbabwe marketing also has smooth tiered stones. These observations narrow the claimed differences without removing any user-decision hold.

Open views repeatedly make hinge seating hard to read. Lesotho was independently reopened and remains visually ambiguous; no definite detached part or failed interaction was demonstrated. Passing animation is not proof of physical attachment. Before realistic-mechanism acceptance, resolve this with source/contact evidence and close rear views; do not call it fixed or certified here.

## Limits and next step
No Blender reopen/source parity, sampled collision suite, corrupt-GLB/no-JS fallback, full archive-inventory rerun or physical-phone test. No production docs edits, deployment, paid generation, funds, key, node, mint or sale operations.

`review.html` is a self-contained comparison report, not a replacement model viewer. Its downsized boards are illustrative, not calibrated material/geometry comparisons; use originals for detailed inspection. The next pre-created consolidation card must preserve every hold and present the 17 art-direction decisions to the user. Completion of this QA card releases the graph, not the designs for launch.
