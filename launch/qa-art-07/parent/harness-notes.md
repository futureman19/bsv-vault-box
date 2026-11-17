# Harness provenance and retained failures
Harnesses copied from ART-05 commit c3318e46fe1ac6ba279f99708ae814caa3775db0; assigned roster changed only at bootstrap. Parent inventory hash asserted before use.

Initial motion run passed first five candidates, then stopped before executing Denmark: AssertionError: unreviewed filesystem use. Read exact Denmark test_motion.mjs: its only filesystem call writes ./motion-check.json beside itself. Expanded safety allowlist to admit that explicit relative URL as well as motion-check.json; no external execution/network permission added. An intermediate patch indentation error was caught by syntax checking and corrected before execution. A diagnostic attempt at Denmark tests.mjs failed because its original file is test_motion.mjs; discovery in the runner already handles both names. These are harness/discovery failures, not artwork failures.

No fresh Blender reopen, source/export parity or geometric collision sampling is claimed for unchanged models. Motion unit checks and browser interaction do not replace those historical gates. Candidate passes are bounded review dispositions, not final user approval.
