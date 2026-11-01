"""Pixel checks, documentation, contact sheet and verified marketing-only delivery."""
from pathlib import Path
from PIL import Image,ImageStat
import hashlib,json,shutil,zipfile
R=Path(__file__).resolve().parent;S=R.parent/'iceland-lightweight-v3'
D=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-marketing');D.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before=json.loads((R/'approved-hashes-before.json').read_text());after={str(p.relative_to(S)):sha(p) for p in S.rglob('*') if p.is_file()};assert before==after
names=['01-closed-hero','02-open-hero','03-material-macro'];checks=[]
sheet=Image.new('RGB',(2400,800),(20,22,25))
for i,name in enumerate(names):
 p=R/(name+'.png')
 with Image.open(p) as im:
  im.load();assert im.size==(3000,3000);rgb=im.convert('RGB');stat=ImageStat.Stat(rgb);assert min(stat.stddev)>10
  assert all(hi>lo for lo,hi in rgb.getextrema())
  checks.append({'file':p.name,'dimensions':list(im.size),'bytes':p.stat().st_size,'sha256':sha(p),'channel_mean':stat.mean,'channel_stddev':stat.stddev,'nonempty':True})
  rgb.thumbnail((800,800),Image.Resampling.LANCZOS);sheet.paste(rgb,(i*800,0))
sheet.save(R/'contact-sheet.jpg',quality=94,subsampling=0)
report={'images':checks,'approved_tree_all_files_hash_equal':True,'protected_file_count':len(before),'visual_review':'All three inspected; single camera-only fix to include complete released latch in open hero. Final open render reviewed and accepted. Approved faceted basalt, cyan rim gap and stylized hardware preserved deliberately.'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2))
readme='''# Iceland / Basalt — marketing photography of approved lightweight v3

Three actual Blender renders, each 3000 × 3000 RGB PNG:
- `01-closed-hero.png` — closed three-quarter hero.
- `02-open-hero.png` — actual fully released latch (-80° local X) and fully open lid (-105° local X), exactly the endpoint of approved motion.mjs. Complete silhouette, including raised latch, has 10% vertical margins.
- `03-material-macro.png` — intentional close crop of the original basalt, brass and polished lid.
- `contact-sheet.jpg` — 2400 × 800 overview, no typography.

## Provenance and preservation

Source: `preview/iceland-lightweight-v3/iceland.blend`, not an AI replacement or reconstructed object. Original source is untouched; three separate editable marketing .blend projects are included with packed textures. Original source author.py, refine_source.py, generate.py and motion.mjs were read. Original approved material factors match all nine GLB materials; all three packed texture payloads match the approved GLB byte-for-byte (`source-parity-check.json`). No collectible geometry, textures, UVs or materials were edited. Only studio camera, lighting/world, resolution/samples, output settings and allowed articulated pose changed. The existing source studio floor is retained. No engraving, accessory or collectible decoration was added.

Source and approved GLB/viewer hashes:
'''
for name in ['iceland.blend','iceland.glb','iceland-lightweight-v3.html','viewer.js','viewer.bundle.js','motion.mjs']:
 readme+=f'- `{name}`: { (S/name).stat().st_size } bytes; SHA-256 `{before[name]}`\n'
readme+='''
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
'''
(R/'README.md').write_text(readme,encoding='utf-8')
files=[p for p in R.iterdir() if p.is_file() and p.name!='marketing-manifest.json' and p.suffix in {'.png','.jpg','.blend','.py','.json','.md'}]
for p in files:
 shutil.copy2(p,D/p.name);assert sha(p)==sha(D/p.name)
manifest={p.name:sha(p) for p in files};(R/'marketing-manifest.json').write_text(json.dumps(manifest,indent=2));shutil.copy2(R/'marketing-manifest.json',D/'marketing-manifest.json')
z=D/'boxsv-iceland-marketing.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,6) as out:
 for p in files:out.write(p,p.name)
 out.write(R/'marketing-manifest.json','marketing-manifest.json')
with zipfile.ZipFile(z) as check:
 assert set(check.namelist())==set(manifest)|{'marketing-manifest.json'}
 for name,h in manifest.items():assert hashlib.sha256(check.read(name)).hexdigest()==h
print(json.dumps({'delivery':str(D),'zip_bytes':z.stat().st_size,'images':checks,'hash_preservation':True,'copied_files_verified':len(files),'zip_readback_verified':True},indent=2))
