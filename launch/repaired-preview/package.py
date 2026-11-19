import json,zipfile,hashlib,shutil
from pathlib import Path,PurePosixPath
from build import ROOT,OUT,REPO,MASTER,sha,dump
DEST=ROOT/'delivery';DEST.mkdir(exist_ok=True)
manifest=json.loads((OUT/'manifest.json').read_bytes());rows=manifest['entries']
files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='inventory.json')
inv={p.relative_to(OUT).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert len([x for x in inv if x.startswith('viewers/')])==201
assert {'index.html','review.html','manifest.json','README.md'}<=set(inv)
dump(OUT/'inventory.json',inv)
files.append(OUT/'inventory.json')
zpath=DEST/'boxsv-repaired-collection-v1-hostable.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,p.relative_to(OUT).as_posix())
recovered=DEST/'recovered';assert not recovered.exists(),'Use fresh delivery directory to preserve prior recovery.'
with zipfile.ZipFile(zpath) as z:
 names=z.namelist();assert len(names)==len(set(names))==len(files)
 assert set(names)==set(inv)|{'inventory.json'}
 for name in names:
  p=PurePosixPath(name);assert not p.is_absolute() and '..' not in p.parts
  data=z.read(name)
  if name!='inventory.json':assert {'bytes':len(data),'sha256':sha(data)}==inv[name]
  target=recovered/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
shutil.copyfile(OUT/'review.html',DEST/'boxsv-repaired-collection-review.html')
assert sha((DEST/'boxsv-repaired-collection-review.html').read_bytes())==sha((OUT/'review.html').read_bytes())
report={'zip':str(zpath),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'files':len(files),'uncompressed_bytes':sum(p.stat().st_size for p in files),'standalone_bytes':(OUT/'review.html').stat().st_size,'standalone_sha256':sha((OUT/'review.html').read_bytes()),'recovery_path':str(recovered),'recovered_entries_verified':len(names),'production_base':MASTER,'existing_docs_bytes':sum(p.stat().st_size for p in (REPO/'docs').rglob('*') if p.is_file()),'hold_ids':[e['id'] for e in rows if e['disposition']=='substantive-feature-hold']}
dump(ROOT/'package-report.json',report)
text=f'''# Scoped publication handoff — not deployed

Feature branch: `feature/repaired-collection-preview`.
Production base: `{MASTER}`. Fetch master again before publishing; do not reset or overwrite newer production work.

## Working deliverables

- Hostable folder: `preview/repaired-collection-v1/`.
- Main route: `/collection-preview/index.html` (also directory route `/collection-preview/`).
- Viewer routes: `/collection-preview/viewers/<canonical-id>.html`, **201** files, actual selected bytes.
- Assets: `/collection-preview/art/<id>.webp` (201 existing marketing images) and `/collection-preview/models/<id>.webp` (201 model-poster derivatives).
- Standalone attachment: `review.html`, **{report['standalone_bytes']:,} bytes**, self-contained poster-only comparison; no nonfunctional remote/local viewer links.
- Supporting routes: `manifest.json`, `inventory.json`, `README.md`; folder-local `.gitattributes` is delivery metadata, not a runtime dependency.
- Entire folder: **{report['files']} files / {report['uncompressed_bytes']:,} bytes**.
- ZIP: **{report['zip_bytes']:,} bytes**, SHA-256 `{report['zip_sha256']}`.
- ZIP readback: all {report['recovered_entries_verified']} entries verified and recovered to `launch/repaired-preview/delivery/recovered/`.

The hostable ZIP is a viewer/media bundle, not a clean-source rebuild archive. Editable source and existing full source packages stay pinned in the manifest. Rebuilding this assembly requires the referenced Git objects, Python and Pillow; browser tests require Playwright and Edge.

## Exact additive publication plan

1. In the release-owned checkout, fetch current master and preserve its latest modern-web, six homepage selections, 201 marketing images and claw fixes.
2. Review this feature commit and publication plan. Copy only the complete `preview/repaired-collection-v1/` subtree to a new `docs/collection-preview/` route. Do not merge or replace old `docs/` from an art branch. No homepage, gallery, claw, wallet, custody, sale or manifest edits are required for this standalone preview route.
3. Existing `docs/` measures {report['existing_docs_bytes']:,} bytes in the pinned checkout. New preview adds {report['uncompressed_bytes']:,} bytes. Check current hosting/repository quotas again at publication time. Consider separate static hosting if desired; all links remain relative and complete.
4. Parent/release owner performs publication. This worker pushes FEATURE ONLY. No master push, deployment, funds, wallet permissions or sale activation.
5. After publishing, read back `/collection-preview/manifest.json`, entry HTML, all 201 viewer routes and image hashes against inventory; exercise desktop/mobile search, filters, compare, iframe model open/reset and focus restoration. Preserve existing homepage/gallery/claw behavior.

No navigation link is inserted into production by this card. The isolated preview URL is the bounded publication scope; any later homepage integration needs its own exact scoped change.

## Remaining substantive feature list

'''
for e in rows:
 if e['disposition']=='substantive-feature-hold':text+=f"- **{e['name']}**: {e['issue']}\n"
text+='''
Ordinary finish choices are resolved for preview, not final art approval. Original records remain in `launch/repaired-preview/history/`. New packaging/geometry repairs are separately recorded rather than showing stale historical defects as still active. All collection/release, physical-device, preservation, rights and security gates remain separate. Real-wallet gate waits for the owner at their computer.
'''
(ROOT/'PUBLICATION-PLAN.md').write_text(text,encoding='utf-8');print(json.dumps(report,indent=2))
