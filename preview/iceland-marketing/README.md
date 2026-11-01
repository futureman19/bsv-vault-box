# Iceland / Basalt — marketing photography of approved lightweight v3

Three actual Blender renders, each 3000 × 3000 RGB PNG:
- `01-closed-hero.png` — closed three-quarter hero.
- `02-open-hero.png` — actual fully released latch (-80° local X) and fully open lid (-105° local X), exactly the endpoint of approved motion.mjs. Complete silhouette, including raised latch, has 10% vertical margins.
- `03-material-macro.png` — intentional close crop of the original basalt, brass and polished lid.
- `contact-sheet.jpg` — 2400 × 800 overview, no typography.

## Provenance and preservation

Source: `preview/iceland-lightweight-v3/iceland.blend`, not an AI replacement or reconstructed object. Original source is untouched; three separate editable marketing .blend projects are included with packed textures. Original source author.py, refine_source.py, generate.py and motion.mjs were read. Original approved material factors match all nine GLB materials; all three packed texture payloads match the approved GLB byte-for-byte (`source-parity-check.json`). No collectible geometry, textures, UVs or materials were edited. Only studio camera, lighting/world, resolution/samples, output settings and allowed articulated pose changed. The existing source studio floor is retained. No engraving, accessory or collectible decoration was added.

Source and approved GLB/viewer hashes:
- `iceland.blend`: 260899 bytes; SHA-256 `1a49de24cdcb01b7ea9118f3a02aed26ac9567d7d0d116078870c5190a37eff1`
- `iceland.glb`: 727772 bytes; SHA-256 `3b6ddabbceb35b075bdb2ae87fd0c722b07cc99c9689cd26f45b081e38a3b5a7`
- `iceland-lightweight-v3.html`: 1757676 bytes; SHA-256 `a279fc179dacbe3cea9b3fee1ef5c1d2cd11ac35648e2fb43926477d5474f711`
- `viewer.js`: 5370 bytes; SHA-256 `3e75ad0848a27de2008dc91be872960272eada7fe4255277c3af05db14d5d0e5`
- `viewer.bundle.js`: 595162 bytes; SHA-256 `e3ce30eb9322ba6b402a8747e76b77d2811be284958638ea2a9db6302c4779ef`
- `motion.mjs`: 352 bytes; SHA-256 `e60937298a3a6de9c2fb9522f5f97d893b24eb0ea56abbac1ed3354f9a62d47a`

All original-directory files were hashed before/after, including original reference source and textures; both manifests are included. Reopened marketing projects preserve source mesh coordinates, topology, UVs, material assignments and hierarchy. Runtime render fingerprints additionally verify the full material node inputs and links remain unchanged for each shot. This is source/PBR parity, not a claim that Cycles and the Three.js viewer produce identical pixels.

## Reproduction

From this repository directory:

```sh
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python preview/iceland-marketing/render.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python preview/iceland-marketing/verify_source.py
python preview/iceland-marketing/package_delivery.py
```

If rendering from the delivered folder, append `-- C:/Users/futur/Desktop/bsv-vault-box/preview/iceland-lightweight-v3` to render.py's Blender command. Scripts overwrite marketing outputs only. The verification/packaging scripts expect the repository sibling source layout. Alternatively reopen any included .blend and render with its saved settings; textures are packed. Original source/GLB/viewer are intentionally not duplicated in the marketing ZIP.

Blender 5.2.1 LTS; Cycles OPTIX on NVIDIA GeForce RTX 4060; 64 samples with denoising, adaptive threshold 0.035, 8 bounces. AgX with +0.25 exposure. Neutral/cool key and front fill, mildly warm rim, neutral overhead strip. Exact camera coordinates, orthographic scales, light powers/sizes/colors and world settings are reproducible in render.py; measured final camera values are in render-provenance.json.

## Verification / limitations

All three final images decoded successfully at 3000 × 3000 with nonconstant channel values and substantial pixel variance. Closed/open full evaluated mesh silhouette bounds pass 5% edge-margin checks; macro crop is intentional. All three visually inspected. The first open composition clipped the released latch; one camera-only auto-fit correction resolved this, independently verified numerically and visually. No material or geometry refinement was performed.

This is the approved stylized collectible: faceted basalt, a smooth polished lid, sparse cyan mineral detail, and simplified hardware remain visible. Render lighting differs from browser lighting; no hyperrealism, physical manufacture, functional engineering, minted status, blockchain custody, production readiness or on-chain storage is implied. No animation code changed. No push, deployment, wallet or network action was performed.
