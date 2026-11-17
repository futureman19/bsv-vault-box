# OPS acceptance report

Bounded local OPS deliverable PASS; launch remains HOLD. Runbook: `launch/ops/RUNBOOK.md`. Tools: `recovery.py`, `exercise.py`, `test_recovery.py` in the same directory. No app, art, custody contract or production docs changes.

## Executed

- `python launch/ops/test_recovery.py`: 2 tests PASS, including 12 invalid portable path inputs and duplicate/missing/tampered/symlink archive cases. `unit.txt`.
- `python launch/ops/exercise.py --output evidence/ops/drill-03`: 14 grouped checks PASS, 4.676 seconds. `drill-03/report.json`, `drill-03.txt`.
- Source commit `01225c6aa893122525116dcfa793ac1f3d6885ae`: all 96 parent evidence file hashes compared to actual committed Git blobs; source inventory hash checked. Backup includes those files plus inventory (97 total).
- Every restored file read back; actual restored SQLite audited through `launch/mint/dry_run.py`, valid seven-event history and event tip `594b0815bdfa1fabf514c6e01ce2e1add9bd856b04e22381a4d81a2d21e15181`. SQLite backup API snapshot passed integrity_check and identical audit. No live database copied.
- `python launch/ops/recovery.py verify --archive evidence/ops/drill-03/rehearsal-backup.zip --expected-sha256 c9a94473b506de18b498fa1a57393053e1113ca40ebc562bd0f002388d52e635`: 97 files verified.
- Local simulated release uses actual index.html, box-demo.html, gallery.html from parent pin and fetched master `606147d6a1521adf635d79a70785ba7f82dbbf77`. Candidate switch/rollback restored exact pointer; corrupt candidate refused; original fixture ledger bytes unchanged. No Pages deployment, full asset restoration or browser recheck claimed.
- Error budget calculated with Python: 30*24*60*0.001 = 43.2 minutes.
- Initial drill-01 exited 1 on guessed nonexistent HTML filenames. Discovered actual files, corrected harness, preserved prior directory. Drill-02 passed, final portable-path-hardened drill-03 passed. No initial all-green claim.

Archive `drill-03/rehearsal-backup.zip` SHA256 **c9a94473b506de18b498fa1a57393053e1113ca40ebc562bd0f002388d52e635**. It contains pinned parent nonsecret fixture evidence, not 201 complete model payloads, keys, dependencies or production state. Hash authenticity requires an independently trusted channel. Raw evidence is marked -text to preserve Git bytes. Failed/restored/negative fixtures stay local and ignored; final reports and original nonsecret backup are retained.

## Remaining scope

Monitoring thresholds, retention/RTO, on-call and release procedures are documented proposals, not provisioned services or proven production controls. Online backup, external checkpoints, key recovery, automatic service suspension/resumption and actual Pages rollback remain unimplemented/unexercised. No keys, RPC, node, real funds, provisioning, purchase, mainnet, sale activation or master push.

Preserve all parent blockers: missing continuous allocation/design/origin/buyer binding, real signing/payment/custody, full-art storage and provenance, compatibility/security review, 73 art/package holds and zero final approvals. All 201 one-of-ones retain equal scarcity. USA v9 is not approved. Parent visual limits remain: mobile overlay interference, missing settled desktop prize evidence, lazy gallery capture not completeness proof, no physical-phone/Safari/deployed acceptance. No images or models changed in OPS, so no new visual verdict.

Next: existing independent FINAL QA `t_85a25a3c` consumes this exact feature ref, reruns critical offline checks in a fresh output directory and consolidates implementation gaps separately from owner decisions. Completion releases that review, not launch authorization.
