# Angola v1 — Miradouro da Lua

Open `angola-v1.html` directly in Edge/Chrome. All runtime assets are embedded: no server or network needed. Drag/touch to rotate, open/close the lid, reset; reduced motion is supported. Cosmetic movement only, not a custody action.

## Delivery
- HTML: **2,728,292 bytes**, strictly below 5,000,000.
- GLB: **1,492,748 bytes**, portable geometry and embedded generated maps.
- `angola.blend`: editable Blender source; `mechanism.blend`: inherited trimmed mechanical baseline.
- `poster.png` and JPEG: actual source render, not AI promotional imagery. Desktop/mobile PNGs are actual offline browser captures.
- `inventory.json`: exact byte counts and SHA-256; `delivery-check.json`: archive readback verification. `angola-v1-source.zip` contains required source, GLB, standalone HTML, maps, scripts and evidence, excluding build dependencies/backups.

## Verified independently on recovery
`python recheck.py` passed build, motion, source, parity, theme, browser and extended gates. Raw outputs are `recheck-*.txt`; earlier outputs are retained separately.

Actual GLTFLoader: 54 meshes, 15,692 triangles, 4 materials, zero nonfinite vertices and zero degenerate triangles. Three eroded ridge groups belong to the lid, each within the brief's relief envelope. Four seam sections are at most 0.090000004 units high. Baseline pivot positions match exactly. Missing-cliff negative control and three invalid-asset controls are rejected by real assertions.

Saved-source reopen: 19 moving and 35 static meshes, 81 poses, zero unintended sampled surface intersections. Every moving ornament is included; only explicit mating hinge leaf/barrel and latch knuckle/bridge/pin surfaces are exempt. Ten hinge attachment pairs intersect as intended. Hollow-floor ray reaches z=0.2650000155. Maximum bidirectional source/export world-vertex discrepancy: 1.712013073529306e-7 units, below 1e-5.

Offline file:// Edge at desktop 1440×1080 and touch-emulated mobile 390×844: actual drag/touch rotation, open/close, interrupted reset, reduced motion, no overflow, zero external HTTP requests or runtime errors. All full-open projected vertices fit (maximum absolute NDC 0.892365). Actual corrupted embedded GLB reaches the real parser and produces the poster fallback; JavaScript-disabled poster also passes. RTX 4060 desktop GPU; not a physical-phone performance test.

## Visual verdict and limitations
Warm sediment-inspired body, brass hardware and three multi-crested lid ridges are visible in source and runtime. The model is intentionally stylized, not a geographic reconstruction, photographic scan or hand sculpture. The regular wavy strata can read as wood grain or decorative resin; the ridge relief is simpler and less deeply eroded than the real landscape. The dark seam is conspicuous. Rear and interior are authored extrapolations. No claim of photoreal equivalence, continuous collision freedom, manufacturing suitability or real-phone FPS.

The earlier run retained initial screenshots, then darkened the earth palette and broadened pinched ridges. Recovery preserved that bounded final design rather than restarting art direction. A real recovery build failed with MODULE_NOT_FOUND because the supplied shared node_modules contained no esbuild. Installing the unchanged pinned dependencies only in this directory fixed it; `initial/recovery-build-failure.txt` records the diagnosis. No acceptance threshold was relaxed. Optional Codex in the prior run failed authentication without accepted edits; recovery verification was run directly by Hermes.

## Reproduce
Requirements: Blender 5.2.1; Python with Pillow/numpy/playwright; installed Edge; Node.js. `npm ci --ignore-scripts --no-audit --no-fund` in this directory restores pinned build-only dependencies. Runtime HTML needs none of them.

1. `python maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python author.py`
3. `python recheck.py` (edit its explicit Windows Blender/Node paths for another system).
4. `python package_delivery.py`

`author.py` is the final generator; `prepare_author.py` is historical initial scaffolding and would overwrite final refinements, so do not rerun it. Regeneration overwrites source/export/poster; preserve manual edits in a separate copy. Shared base kit and other previews are unchanged. Local `* -text` Git attributes preserve inventoried bytes across checkout.

Research is cited in `design-brief.md`; the original Atlas Obscura erosion/colored-strata description was independently reconfirmed during recovery. No source photography or sacred motifs were copied. Three.js 0.180.0 is MIT; license included. Source/mechanism/viewer lineage is the existing Japan/Iceland pilots.

Art-only branch backup, not a deployment or mint. No blockchain node, keys, chain queries, transactions, production website changes or VPS access. Proposed collection remains 201 equally one-of-one designs; media storage and signed authenticity are not implemented by this preview. Per-asset human review was explicitly waived; final collection integration is separate.
