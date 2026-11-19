"""Verify retained gates, preservation, read-only inspection and evidence byte inventory."""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
checks={}
for name,count in [('final-tests',11),('parents-regression',54),('mint-posix',187),('security-regression',10)]:
 text=(OUT/(name+'.txt')).read_text(encoding='utf8')
 assert re.search(r'(?:#|ℹ) pass '+str(count)+r'\b',text)
 assert re.search(r'(?:#|ℹ) fail 0\b',text);checks[name]=count
assert '111 passing' in (OUT/'vm.txt').read_text(encoding='utf8');checks['vm']=111
assert 'Ran 19 tests' in (OUT/'allocation.txt').read_text();checks['allocation']=19
assert (OUT/'typecheck.txt').stat().st_size==0;checks['typecheck']='exit 0; empty output'
for file in ['replay-cli.txt','replay-browser-desktop.txt','replay-browser-mobile.txt']:
 text=(OUT/file).read_text(encoding='utf8')
 start=text.index('{')
 prefix=text[:start].strip().splitlines()
 assert all(re.fullmatch(r'\(node:\d+\) ExperimentalWarning: SQLite is an experimental feature and might change at any time|\(Use `node --trace-warnings \.\.\.` to show where the warning was created\)',line) for line in prefix), prefix
 p=json.loads(text[start:]);assert len(p['transitions'])==5;assert all(t['serializedVM'] for t in p['transitions']);assert all(p['provenance'].values());assert p['chainInclusion'] is False
browser=json.loads((OUT/'browser-02/report.json').read_text());assert browser['result']=='PASS' and not browser['external_requests'] and not browser['page_errors'];checks['browser_grouped_checks']=len(browser['checks'])
refs=[('db4760ddcb33108da563b1df84a7e308205de3ec','evidence/final-qa'),('d02b279d8ea41871c4f4af6760576a3926617fb6','evidence/continuous'),('f0a54d9b3e80338fbe34c869987a45d6d23ae25c','launch/collection')]
for ref,p in refs:subprocess.run(['git','diff','--exit-code',ref,'--',p],cwd=ROOT,check=True,capture_output=True)
checks['preserved_refs']=refs
file=OUT/'run-01/delivery.sqlite';before=sha(file.read_bytes())
r=subprocess.run(['node','mint/scripts/delivery-inspect.js',str(file),'box-1','launch/continuous/paid-config.json'],cwd=ROOT,capture_output=True,check=True)
assert sha(file.read_bytes())==before
checks['read_only_delivery_sha256']=before;checks['read_only_exit']=r.returncode
bundle=ROOT/'launch/continuous/browser/wallet.js';checks['executed_browser_bundle']={'bytes':bundle.stat().st_size,'sha256':sha(bundle.read_bytes())}
sources={}
for p in sorted((ROOT/'launch/continuous').glob('*')):
 if p.is_file() and p.suffix in ['.js','.py','.json','.html','.css','.md']:sources[p.relative_to(ROOT).as_posix()]=sha(p.read_bytes())
for f in ['vault/src/ordinal-pair.js','vault/src/launch-record.js','vault/artifacts/ordinalPair.json','mint/delivery.js','launch/wallet-transport/adapter.js','launch/wallet-transport/package-lock.json']:
 sources[f]=sha((ROOT/f).read_bytes())
checks['executed_sources']=sources
checks['checkout_newline_differences']={}
for name,digest in sources.items():
 staged=subprocess.check_output(['git','show',':'+name],cwd=ROOT)
 working=(ROOT/name).read_bytes()
 if sha(staged)!=digest:
  assert working.replace(b'\r\n',b'\n')==staged.replace(b'\r\n',b'\n'), name
  checks['checkout_newline_differences'][name]={'executed_sha256':digest,'git_sha256':sha(staged),'newline_only':True}
(OUT/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
files={p.relative_to(OUT).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='sha256.json'}
(OUT/'sha256.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'checks':checks,'evidence_files':len(files)},indent=2))
