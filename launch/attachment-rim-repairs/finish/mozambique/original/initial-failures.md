# Actual initial verification failures

- Optional Codex CLI exited 1: HTTP 401/token refresh failed. No accepted edits; direct Hermes implementation used instead. No credential changes.
- Shell `node --test` exited 1 with `stdin is not a tty`; invoking the native executable directly passed both tests.
- First browser verification failed at verify_browser.py line 33: reduced-motion Reset after a fixed 60ms wait had not yet published progress=0. Changed the harness to wait for the observed pose (bounded 2 seconds), rather than assuming desktop rendering latency. Interaction and pose assertions remain unchanged. Subsequent results are in browser-check.json.
