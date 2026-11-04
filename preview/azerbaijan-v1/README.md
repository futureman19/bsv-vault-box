# Azerbaijan v1 — Lahij Copper

Open `azerbaijan-v1.html` directly in Edge/Chrome. Fully embedded 3D model, runtime, textures and actual Blender-render poster; no network needed. Drag/touch rotate, Open/Close, Reset and reduced-motion support. Cosmetic movement only; not minted, deployed, hosted or custody verification.

## Delivered / verified
- HTML: **2,821,773 bytes**; GLB: **1,495,300 bytes**. Strict HTML budget <5,000,000.
- Editable packed `azerbaijan.blend`, standalone `azerbaijan.glb`, deterministic maps and authoring scripts. `mechanism.blend` is the unchanged trimmed Japan pilot mechanism; no cedar/tree artwork reused. Shared vault kit untouched.
- Source independently reopened: **81 sampled poses**, all **28 moving / 35 static meshes**, no unintended surface intersections. Explicit bearing exclusions only. Ten physical hinge attachment pairs intersect. Hollow liner floor ray hits z=0.265. This is sampled surface-intersection evidence, not continuous collision/manufacturing certification.
- Actual loader: **63 meshes, 13,804 triangles, four materials**, zero nonfinite vertices or degenerate triangles. Source/export maximum nearest-vertex error **1.712013073529306e-7** (limit 1e-5); packed color/normal/roughness maps verified. Roughness decoded in glTF green channel.
- Theme: eight separate abstract raised leaves, two rings, 0.76-radius medallion; all relief lid-owned, below 0.22 above lid. Exact inherited pivot matrices preserved. Deliberate missing-leaf negative control rejected; motion tests also reject invalid assets and wrong endpoint sequencing.
- Offline `file://` Edge desktop 1440×1080 and mobile touch emulation 390×844: drag/touch, native open/close, interrupted reset, reduced motion, no horizontal overflow, zero external HTTP requests and JS errors. Full-open projection max absolute NDC 0.892365. Actual corrupt-GLB parser failure displays poster and disables controls; no-JS poster checked. RTX4060 desktop GPU, not a physical phone benchmark.
- `inventory.json` records exact payload byte counts and SHA-256; `delivery-check.json` records ZIP entry/readback validation. Archive excludes dependencies, caches and .blend backups. Folder-local Git attributes preserve exact bytes.

## Visual verdict and scope
Research-backed Lahij copper-craft interpretation, **not artisan-made, photorealistic or a reproduction of a historic pattern**. The brief predates modeling and cites UNESCO. Eight angular leaf forms are intentionally invented and read as a geometric rosette. Broad procedural mottling approximates hammered copper but can look grainy; brass is simplified, the dark seam is visually pronounced, and render noise remains. Mobile closed/open framing is readable; fine relief is less obvious at mobile scale. From the front at full opening the exterior relief naturally faces away; ownership is verified numerically. Small hinges are difficult to judge in the mobile image, so source contact checks are reported separately, not as visual engineering certification.

No source/art acceptance failures occurred in this first direct implementation. An optional Codex helper failed authentication before making any edits; its diagnostic is retained, and all implementation and verification were performed directly by Hermes. Local build dependencies were installed from the inherited pinned package manifest because the prescribed shared installation lacked esbuild. No credentials were accessed or changed. `setup.py` records initial scaffold provenance; do not rerun it after customizing files. No human approval is claimed; this card explicitly waived per-asset review until collection assembly.

## Reproduce
Python with numpy, Pillow and Playwright; installed Edge; Blender 5.2.1; Node.js build tooling (not a blockchain node). `npm ci --prefix preview/azerbaijan-v1 --ignore-scripts --no-audit --no-fund` from repository root restores pinned local build dependencies. Source authoring otherwise needs only this folder.

From repository root:
1. `python preview/azerbaijan-v1/maps.py`
2. `blender --background --factory-startup --python-exit-code 1 --python preview/azerbaijan-v1/author.py`
3. Run Blender with each of `verify_source.py`, `verify_parity.py`, `verify_theme.py` using the same flags.
4. `python preview/azerbaijan-v1/build.py`
5. `node --test --test-reporter=tap preview/azerbaijan-v1/tests.mjs`
6. `python preview/azerbaijan-v1/verify_browser.py` and `python preview/azerbaijan-v1/verify_extended.py`
7. `python preview/azerbaijan-v1/package_delivery.py`

Authoring overwrites generated source/render/model; preserve manual edits separately. Regeneration requires refreshing inventory. Three.js runtime is MIT; license included. Research text was used for factual inspiration only; no third-party photos/textures embedded. Collection direction remains 201 equal-scarcity one-of-one designs. Next: separate final integration card merges branches and assembles the collection gallery; no merge is performed here.
