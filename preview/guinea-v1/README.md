# Guinea v1 — Nimba highland

Open `guinea-v1.html` directly in Edge/Chrome. Entire offline viewer: **3,580,154 bytes**; standalone GLB: **2,105,112 bytes**. Drag/touch rotation, staged opening/closing, Reset and reduced-motion support. Cosmetic inner collectible only; not minted, hosted, signed or chain-verified.

## Design and provenance
The pre-model `design-brief.md` cites UNESCO's Mount Nimba reserve description: dense lower forest and grassy mountain pastures above savannah on the Guinea/Liberia/Côte d’Ivoire borders. The source was rechecked through web search during recovery. This transboundary landscape is not exclusive to Guinea. Three unequal stylized ridges, clustered lower greenery, earth-red mineral body and brass fittings interpret that landscape; not a geographic survey, traditional craft claim or photogrammetry. No research imagery is embedded.

The editable `guinea.blend`, exported `guinea.glb`, generated maps and actual-source `poster.png` accompany the self-contained HTML. Mechanism lineage is the read-only Japan pilot's trimmed mechanism; shared vault kit and prior previews remain untouched. Three.js 0.180.0 MIT license included; esbuild 0.25.11 is build-only.

## Verified
- Independent saved-source reopen: hollow floor ray z=0.2650000155; ten connected hinge attachment pairs.
- 81 opening samples: all 59 moving and 39 static meshes; no unintended surface intersections. Latch versus lid included; only named mating bearings exempted. This is sampled BVH intersection evidence, not continuous collision/manufacturing certification.
- Latch releases 80 degrees before lid opens 105 degrees. All ridge/forest ornamentation travels with Lid_Hinge. Theme dimensions 2.4600 × 0.9600 × 0.67975, three unequal peaks and 42 forest clusters; narrow seam 0.108.
- Independent source/export nearest-vertex error 1.712013073529306e-7, below 1e-5 tolerance.
- Real GLTFLoader: 100 meshes, 19,404 triangles, eight materials; zero nonfinite vertices or degenerate triangles. Portable decoded map variation and terrain ancestry tested.
- Actual offline file:// Edge: desktop and 390×844 touch emulation, native controls, drag/touch rotation, open/close, interrupted Reset, reduced motion, no horizontal overflow, no external HTTP requests, no unexpected runtime errors. Full-open maximum absolute NDC 0.892365. Actual corrupt GLB parser failure and no-JavaScript poster fallback pass.
- Browser mobile runs on desktop RTX 4060: not physical-phone testing or performance certification. Closed/open/rear screenshots are actual renders, not promotional illustrations.
- Motion tests include 81 poses and deliberately invalid asset inputs. Inventory and ZIP are read back and hash-checked; directory-local Git attributes preserve exact bytes.

## Recovery and honest limitations
The interrupted first run exported source/GLB but failed rendering with OIDN out-of-memory (`author-output.txt`). Recovery disabled denoising, bounded rendering to four threads at 900×820, and regenerated a genuine source poster; mild render noise remains. Terrain perimeter faces were closed into the lid. The first extended browser probe missed the ridge's multi-material child meshes and failed its terrain-count assertion (`extended-initial-failure.txt`); the corrected probe follows terrain ancestry without lowering the required count. All final gates pass.

Visual inspection confirms three readable peaks and unclipped mobile framing. Material reads as mottled pink/brown mineral but can also resemble wood; terrain is simple and angular, the green gasket remains conspicuous, brass is cleaner than aged real fittings. This is a stylized first-version collectible, not photoreal-equivalent or human-approved final artwork. Per-asset human review was explicitly waived for this batch.

The optional Codex lane in the original attempt failed authentication; no Codex changes were accepted. Recovery implemented and verified directly. Shared dependency directory was empty, so exact pinned dependencies were installed only inside this new folder; node_modules is excluded.

## Reproduce
Requires Blender 5.2.1, Python with Pillow/numpy/playwright, installed Edge, Node and the pinned npm dependencies. From this folder: `npm ci --ignore-scripts --no-audit --no-fund`; `python maps.py`; run Blender `--background --factory-startup --python-exit-code 1 --python author.py`; `python build.py`. Run Blender similarly on `verify_source.py`, `verify_parity.py`, `verify_theme.py`; run `node tests.mjs`, `python verify_browser.py`, `python verify_extended.py`, then `python package_delivery.py`. Authoring overwrites generated source: preserve manual edits separately. `prepare.py` is historical seeding only, depends on the sibling Japan pilot, and would overwrite later corrections; do not run it to rebuild this delivery.

No wallet, blockchain node, keys, minting, funds, deployment, VPS changes or integration performed. Branch backup only; collection integration belongs to the downstream card.
