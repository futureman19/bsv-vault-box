# Sri Lanka / Dumbara Weave — v1

Open `sri-lanka-v1.html` in Edge/Chrome directly, offline. Drag/touch rotation, zoom, Open/Close and Reset work without a server. This is cosmetic collectible art, not a minted token, custody system, sale, or on-chain storage.

## Delivery
- HTML: **4,209,106 bytes**, strictly below 5,000,000; embedded Three.js runtime, GLB, portable maps and actual-source JPEG poster.
- GLB: **2,549,052 bytes**.
- `sri-lanka.blend`: packed editable procedural Blender source; `mechanism.blend`: copied reusable Japan mechanical scaffold.
- `maps/`: original generated colour and roughness maps, not scans. No research images copied.
- `poster.png` / `.jpg`: actual source render. `desktop-*` / `mobile-*`: actual offline browser captures.
- `inventory.json`, `delivery-check.json`, and source ZIP: exact-byte/hash inventory and archive readback. `.gitattributes` preserves bytes across Git checkout.

## Design and visual limits
The prewritten brief cites UNESCO documentation of Sri Lankan Dumbara hana-fibre weaving and its ivory/red/yellow/black palette. The box translates that craft inspiration into dark timber framing, large ivory patterned panels and three invented nested raised diamond ornaments. It is not traditional artisan work, a faithful symbolic pattern, or community-endorsed design.

Actual source and mobile images show all three ornaments, seated panels and complete framing. Fine weave reads partly as ribbing on mobile; timber is visibly procedural. The narrow dark seam is visually conspicuous, render noise remains, and nested ornament edges are angular. The long inherited staged latch and exposed rear hinges are family extrapolations, not craft research. The open front view makes some small connections visually ambiguous, although all ten hinge attachment intersections were independently checked. This is a stylized collectible, not photorealistic or mechanical/manufacturing certification.

## Verified
- Independent saved-source reopen: 65 moving and 103 static meshes; 81 opening samples; zero unintended sampled intersections. Includes all new ornament segments. Only named mating hinge barrel/leaf and latch knuckle/bridge/pin bearings exempt. Interior floor ray z=0.2650000155. Ten hinge attachment pairs checked.
- Independent GLB import versus saved source: bidirectional nearest-vertex maximum error 1.712013073529306e-7 (<1e-5). Three packed source images.
- Actual browser GLTFLoader: 168 meshes, 29,336 triangles, nine materials, zero nonfinite vertices or degenerate triangles.
- Independent theme test: 36 raised segments across three open diamond centres, lid ancestry, surface seating and bounded ornament dimensions, four broad panels, narrow seam, exact inherited evaluated pivot matrices. A deliberately detached in-memory ornament is rejected; this is a negative control, not a production defect.
- Offline file:// desktop 1440x1080 and mobile touch emulation 390x844: rotation, native controls, open/close, interrupted reset, reduced-motion endpoints, no overflow, no external HTTP requests or console/page errors. Full-open maximum absolute NDC 0.9156477401. Real corrupt GLB reaches loader failure and poster fallback; no-JS poster separately tested. RTX 4060 desktop GPU, not physical-phone performance.
- Decoded portable map variation checks use roughness GREEN channel, dimensions <=512. Viewer visible and accessibility copy checked for correct country.
- Motion tests exercise clamped endpoints, sequential 80-degree latch / 105-degree lid choreography and invalid-asset rejection.

## Failures and provenance
No model acceptance failure occurred during the first direct implementation. The optional Codex lane failed with HTTP 401/token-refresh failure before edits; `lane-output.txt` preserves that tooling failure. Hermes implemented directly without touching credentials. The existing shared compiler directory was empty, so the unchanged pinned Three 0.180.0 and esbuild 0.25.11 were installed only within this new directory. Node modules are excluded. Direct web extraction was unavailable; research references were retrieved through web search. No false failure-and-fix is claimed.

## Reproduce
Python with numpy, Pillow, Playwright; installed Edge; Blender 5.2.1; Node.js. Restore build dependencies with `npm ci --prefix preview/sri-lanka-v1 --ignore-scripts --no-audit --no-fund`. All commands from repository root:

1. `python preview/sri-lanka-v1/maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python preview/sri-lanka-v1/author.py`
3. `python preview/sri-lanka-v1/verify_all.py`

`verify_all.py` rebuilds the viewer, reruns motion, source, parity, theme, browser and extended tests, then packages and verifies the ZIP. It does not reauthor or rerender. `setup.py` documents initial adaptation from the read-only Japan pilot; do not rerun it over final refinements. Source authoring itself uses the included mechanism and maps. Regeneration overwrites generated files; make separate copies for manual edits. The verification wrapper defaults to this machine's discovered Blender path; set BLENDER to override. Three.js license included.

Only this asset directory is added. No shared kit or other preview was modified. No nodes, keys, chain queries, minting, broadcasts, VPS, public website or production deployment. Branch backup only; collection integration is a separate downstream card.
