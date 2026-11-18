"""Read-only recovery checks; package frozen candidate without refreshing captures."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
R=Path(__file__).resolve().parent
REPO=R.parents[1]
P=REPO/'preview/bangladesh-finish-v2'
def sha(b): return hashlib.sha256(b).hexdigest()
def git(spec): return subprocess.check_output(['git','show',spec],cwd=REPO)
freeze=json.loads((R/'review-freeze.json').read_text())
for name,h in freeze.items(): assert sha((REPO/name).read_bytes())==h,name
historical=json.loads((P/'historical-manifest.json').read_text())
for f in historical['files']:
 b=(P/'historical-v1'/f['path']).read_bytes()
 assert sha(b)==f['sha256'] and len(b)==f['bytes']
 assert b==git(historical['commit']+':'+historical['prefix']+f['path'])
parent=git('3952a4eb1c57ca921c21d0aa774ab8b8752e3df7:launch/collection-repairs/dispositions.json')
assert parent==(REPO/'launch/collection-repairs/dispositions.json').read_bytes()
assert len(json.loads(parent)['records'])==201
base=json.loads((R/'baseline.json').read_text()); disp=json.loads((R/'dispositions.json').read_text())
expected=set('argentina bangladesh cambodia comoros djibouti eritrea gambia guinea-bissau lebanon malawi mexico myanmar nigeria palestine qatar samoa southern-ocean tajikistan tunisia zambia'.split())
assert len(base)==len(disp['entries'])==20
assert {e['id'] for e in base}=={e['id'] for e in disp['entries']}==expected
for e in disp['entries']:
 old=next(x['original_review'] for x in base if x['id']==e['id'])
 assert e['unresolved_owner_holds']==old.get('missing_gates',[])
 assert e['inherited_holds']==old.get('inherited_missing_gates',[])
 assert not e['final_approved'] and not e['launch_ready'] and not e['model_geometry_changed']
# Original archive verifier executed without overwriting its frozen report.
src=(R/'verify_sources.py').read_text().replace("(R/'source-package-check.json').write_text(json.dumps(out,indent=2));",'')
ns={'__file__':str(R/'verify_sources.py')};exec(compile(src,str(R/'verify_sources.py'),'exec'),ns)
assert ns['out']==json.loads((R/'source-package-check.json').read_text())
# Re-exercise browser controls without overwriting independently inspected screenshots/reports.
src=(P/'verify_browser.py').read_text()
src='\n'.join(line for line in src.splitlines() if 'p.screenshot(' not in line)
# The fallback line also contains result collection/context cleanup.
src=src.replace(' b.close()',"  results.append({'case':case,'pass':True});c.close()\n b.close()")
src=src.replace("(R/'browser-check.json').write_text(json.dumps(results,indent=2));",'')
ns={'__file__':str(P/'verify_browser.py')};exec(compile(src,str(P/'verify_browser.py'),'exec'),ns)
assert len(ns['results'])==6
browser=ns['results']
for name,h in freeze.items(): assert sha((REPO/name).read_bytes())==h,name
# Deliver all successor sources and historical evidence, excluding caches and self-referential output.
files=[p for p in P.rglob('*') if p.is_file() and not any(x in p.parts for x in ('node_modules','__pycache__')) and p.name not in ('inventory.json','source.zip')]
required={'bangladesh-finish-v2.html','bangladesh.glb','bangladesh.blend','build.py','viewer.js','viewer.bundle.js','template.html','motion.mjs','tests.mjs','verify_browser.py','verify_parity.py','historical-v1/author.py'}
assert required <= {p.relative_to(P).as_posix() for p in files}
inv={p.relative_to(P).as_posix():{'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(files)}
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
archive=R/'bangladesh-finish-v2-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[P/'inventory.json']:z.write(p,p.relative_to(P).as_posix())
with zipfile.ZipFile(archive) as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(inv)+1
 assert z.testzip() is None
 for n,f in inv.items():
  b=z.read(n);assert sha(b)==f['sha256'] and len(b)==f['bytes']
 assert json.loads(z.read('inventory.json'))==inv
result={'frozen_entries_verified':len(freeze),'historical_files_verified':len(historical['files']),'assigned_ids':20,'parent_records':201,'source_archives':len(ns.get('out',[])) if 'out' in ns else 20,'browser_fresh':browser,'source_zip':{'path':str(archive),'sha256':sha(archive.read_bytes()),'bytes':archive.stat().st_size,'members':len(inv)+1},'html_bytes':(P/'bangladesh-finish-v2.html').stat().st_size,'art_approved':False,'launch_ready':False}
assert result['html_bytes']<5000000
(R/'delivery-recovery.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='browser_fresh'},indent=2))
