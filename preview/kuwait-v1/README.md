# Kuwait v1 — Sadu & Sand

Open **kuwait-v1.html** directly in Edge/Chrome. Everything needed at runtime is embedded: the model, maps, Three.js and a poster rendered from the actual Blender source. Drag/touch to rotate; Open/Close lid; Reset view. Cosmetic art only; no wallet, custody change, network download or transaction.

## Delivered
- **HTML: 2,822,646 bytes** (strictly below 5,000,000).
- **GLB: 1,590,904 bytes**; 76 meshes, 19,594 triangles, five materials.
- `kuwait.blend`: editable named parts, packed generated maps, studio/camera. `mechanism.blend` is the included read-only-lineage mechanism input.
- `maps/`: four original procedural maps, at most 512px. No scans, copied photographs, tribal insignia, or AI promotional replacements.
- `poster.png` / `poster.jpg`: actual Blender render. Desktop/mobile closed/open, rear-open and fallback screenshots are actual offline browser captures.
- `design-brief.md`: written before modeling, with UNESCO research and measurable contract. Al Sadu is shared regional heritage; this design does not claim it is exclusively Kuwaiti or that these invented diamonds are authentic traditional symbols.
- `kuwait-v1-source.zip`: editable source, standalone HTML/GLB, maps, scripts, screenshots, checks and license. `inventory.json` lists exact bytes and SHA-256 for payloads; `delivery-check.json` verifies ZIP contents and bytes on readback. Those two manifests and the ZIP intentionally do not hash themselves recursively.

## Verified, with limits
`run_checks.py` runs the bounded acceptance suite and fails on any nonzero command:
- Motion: 80-degree latch release in first quarter, then 105-degree lid opening. Reverse is the same progression backwards. Endpoint, staging, monotonicity, clamping and invalid-geometry controls pass.
- Saved Blender source independently reopened. Pivots' local matrices exactly match the included inherited mechanism. Hollow floor ray hits Z 0.265; ten explicit hinge attachment pairs intersect as intended.
- **81 sampled poses, 21 moving meshes versus 55 static meshes**, plus releasing latch versus moving lid, zero unintended surface intersections. Recursive moving-part ancestry includes the dune and all lid textile strips. Only named mating bearing contacts excluded. This is sampled surface-intersection evidence, not continuous collision/manufacturing certification; rigid parts within the same moving assembly are intentionally joined/overlapping.
- Source/export bidirectional nearest-vertex error **1.712013073529306e-7**, below 1e-5. This proves geometric point-set parity, not byte-identical export or material-render equivalence.
- Actual GLTFLoader: zero nonfinite vertices and degenerate triangles; finite UVs; four decoded maps with variation. Roughness checked in the glTF **green** channel. One lid-parented dune relief, eight textile panels/strips; three crest peaks along actual source centreline. Dune footprint 2.5 × 1.3, top Z 2.30577 above the lid's nominal Z 1.978.
- Offline **file://** desktop 1440×1080 and mobile 390×844 touch emulation: native click/tap, mouse/touch drag, open/close, interrupted reset, reduced motion, zero external HTTP requests, zero unexpected runtime errors and no horizontal overflow. Whole open silhouette projects inside viewport (maximum absolute NDC 0.892365). Actual corrupted GLB reaches parser and displays poster; JavaScript-disabled poster also checked.
- Texture palette/diamond rhythm and nonblank source poster checks. Flat texture and detached-ornament negative controls are rejected. They are post-implementation regression controls, not claimed as pre-model TDD.

Browser uses desktop Edge/RTX 4060. Mobile emulation is **not** physical-phone performance testing. No FPS, photorealism, museum-accurate textile, mechanical manufacture, minting, public hosting or on-chain storage claim.

## Visual result and bounded corrections
The strong red/charcoal/ivory horizontal diamonds read clearly on desktop/mobile. Dark wood framing and satin brass preserve the family silhouette. Sand relief is a low, smooth, three-crest sculpt, deliberately not a named landmark. Source-render and browser visual inspection found all core features and no major clipping/assembly defect. Remaining limits: patterned panels read more graphic than fibrous; regular wood grain is stylized; pale dune contours are soft and can resemble a sculpted cushion at small sizes; lid border reads mostly red; some panel diamonds are naturally cropped by the frame. The rear-open screenshot exposes the outside of the lid, hidden from the normal front-open view. This is a coherent procedural v1, not photoreal equivalence or human art approval.

Two real technical failures retained in `initial/`:
1. First 1100×1000 source render returned allocation warnings and a transparent black PNG despite Blender exit 0. Pixel acceptance rejected it. Regenerated the actual source at 800×720, 16 samples, two render threads, with inherited compositing disabled; the final opaque, nonblank render passes. No substitute marketing image used.
2. Initial texture check incorrectly read roughness from red, reporting zero range. Corrected to glTF's specified green channel, retaining the same variation threshold; decoded roughness now passes.

The optional Codex lane exited with authentication 401 before implementing anything. Hermes directly authored, tested and packaged all work; no credential files were touched. `codex-lane-result.json` records that outcome.

## Rebuild
From this directory, with Python (numpy, Pillow, Playwright), installed Edge, Blender 5.2.1, Node.js and Three/esbuild from `package.json`:

```text
python maps.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python author.py
python run_checks.py
python package_delivery.py
```

`author.py` loads local helper/studio text files and local `mechanism.blend`. Regeneration overwrites manual edits; save those separately. Set BLENDER for another executable path. Build uses local node_modules, otherwise the sibling Iceland pilot's installed dependencies. A standalone source extraction needs `npm install` here. The offline HTML requires none of those dependencies. Build scripts and evidence logs contain local toolchain paths; no secrets. Three.js is MIT, license included.

Additive-only under `preview/kuwait-v1/`. Branch backup only, no merge or deployment. Shared kit, other previews and chain-related directories unchanged. Next step: retain this v1 for the final full-collection integration/review; no per-asset review gate.
