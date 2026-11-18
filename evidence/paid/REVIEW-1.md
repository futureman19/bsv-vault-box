# Independent review 1 — do not close
Read-only reviewer deleg_3a0c8d9b independently ran 72 new/continuous tests plus the explicit continuous test, all passed; source diff check passed. It reproduced two blocking issues:
1. Persisted `payment.qualified` could authorize direct Engine Transfer after restart without fresh payment observation. HTTP-only refresh was insufficient, including PREPARED resumption.
2. Receipt history was labeled with an invoice but no enforced unique-address/global receipt allocation prevented reuse across invoices.
It also identified engineering scope gaps, not merely missing user permission: browser signing was server-side fixture only; payment observer/custody constrained to offline/regtest; installed provider compatibility unverified.
No code was changed by the reviewer. Tests green did not override these findings. Correction pass 1 will address the two authorization issues and the configured integration/browser seams. Real installed-extension approval remains forbidden during this run.
