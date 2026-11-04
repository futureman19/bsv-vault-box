# Recovery and bounded corrections
Recovered unfinished authored source and checks after worker infrastructure crashes. All source/theme/parity/browser gates were rerun by Hermes, not accepted from prior reports.

Initial mobile visual inspection found the crater hard to see. Preserved initial-low-camera.png; raised viewer camera Y from 3.7 to 6.2 without changing geometry. Final visual inspection finds a visible but subtle shallow summit depression; not photorealism.

New extended map check initially failed: `TypeError: cannot unpack non-iterable int object` at `ranges=[b-a for a,b in im.getextrema()]`. Grayscale PNG extrema are a single pair. Fixed by converting to RGB before evaluating ranges; retained nonzero variation and 512px gates. This is a test-harness fix, not a model defect.

Research recheck: https://dgff2021.unctad.org/comoros identifies volcanic islands, Karthala and ylang-ylang essence production. https://en.wikipedia.org/wiki/Comoro_Islands describes Karthala as a shield volcano with a large summit caldera. Search text rechecked during recovery; no third-party pixels used. Direct extraction backend unavailable; search retrieval succeeded.

Prior optional Codex lane failed authentication and made no accepted changes (prior task heartbeat records this). No credentials accessed during recovery. All completion work was direct Hermes.
