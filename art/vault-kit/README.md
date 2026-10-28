# BoxSV authored vault kit

Custom **script-authored Blender geometry**, not purchased assets, hand-sculpted artwork, or generated textures. Four texture-free GLBs replace the cabinet structural shell, claw actuator, three articulated finger visuals and six gift-shaped prizes. Source: `vault-kit.blend`, with named, editable parts and non-destructive bevel modifiers in four collections. The parts share their runtime local origins, **not a presentation lineup**: solo a collection in Blender to edit it. Regeneration overwrites manual edits.

## Geometry

- Cabinet: stepped plinth/feet, reinforced chamfered posts, socket plates/hex bolts, pressed rear panels, service panels/louvers and layered crown.
- Claw: tapered actuator housing, collars, hydraulic rods, forged hook profiles, pivot barrels/pins and grip teeth.
- Vault collectible: armored lid/gasket, corner shoes, rivets, side hinges, octagonal lock escutcheon and raised three-spoke rotary lock. Runtime retains the six existing prize colors.

| GLB | Triangles | Material batches | Bytes | Editable parts |
|---|---:|---:|---:|---:|
| cabinet | 6,208 | 5 | 438,856 | 64 |
| claw-hub | 636 | 4 | 41,052 | 13 |
| claw-finger | 700 | 4 | 44,024 | 7 |
| vault-box | 2,288 | 5 | 160,440 | 28 |

Measured through the actual pinned Three 0.186 GLTFLoader, not inferred from source: 684,372 bytes / 9,832 triangles unique; 22,672 authored triangles with three fingers and six boxes. Export copies are merged by material and clones share geometry/materials (only six recolor materials are cloned). No textures, Draco decoder, CDN, or new build step. These are bounded low-poly meshes, not a claim of maximum possible compression.

## Anchor contract

Author game `(x,y,z)` as Blender `(x,-z,y)`; export standard Y-up glTF.

- Cabinet: origin and footprint retained; new crown maximum Y is 3.9735, feet minimum Y .02.
- Hub: local Y -.79 to -.55 beneath the existing claw group.
- Finger: local X .083 to .374, Y -1.2776 to -.673; reuse existing three radial groups and their original X compression animation. This is **rigid grouped articulation, not a skinned/IK or physically simulated new mechanism**.
- Vault: original centered body/base anchor, minimum Y -.235; maximum Y .2985, raised lock front Z .321. Existing prize groups continue to own placement, rotation, attachment, squash and reveal hiding.
- Cable, trolley/carriage, rails, glass, text labels, lights and collection fascia stay in the original renderer. The game controller, control events, 30-second clock, nearest-box rule, prize draw, wallet, payment and crypto code are unchanged.

All four downloads must succeed before visuals switch. Failure of any one keeps the entire original primitive presentation. WebGL failure still uses the original CSS cabinet. Original primitive resources remain allocated until renderer disposal for the fallback path; asset geometry is also disposed, including downloads that resolve after unmount.

## Rebuild / verify (repository root)

```sh
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python art/vault-kit/build.py
"C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe" --background --factory-startup --python-exit-code 1 --python art/vault-kit/verify-source.py
python test/vault-assets-browser.py
python test/vault-video-browser.py
node --test test/*.test.js
python test/python-parity.py
```

See `evidence/vault-assets/README.md` for actual results, visual qualifications, and the preserved failed probes. `docs/` is the actual deployable static artifact; all browser acceptance here is local HTTP, not a deployment. Do not push master to preview this work.
