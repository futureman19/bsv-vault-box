import pathlib,json,subprocess
R=pathlib.Path(__file__).resolve().parent
ids=json.loads((R/'assigned.json').read_text()); es=json.loads((R/'launch-candidates.json').read_text())['entries']; results=[]
for e in es:
 if e['id'] not in ids:continue
 s=e['id']; dest=R/'motion'/s;dest.mkdir(parents=True,exist_ok=True); base=str(pathlib.PurePosixPath(e['viewer']['path']).parent)
 for name in ['motion.mjs','tests.mjs']:
  source_name='test_motion.mjs' if s=='barbados' and name=='tests.mjs' else name
  b=(R/'motion'/'afghanistan'/'tests.mjs').read_bytes() if s=='costa-rica' and name=='tests.mjs' else subprocess.check_output(['git','show',e['selection']['commit']+':'+base+'/'+source_name]); text=b.decode()
  assert not any(t in text for t in ['child_process','fetch(','http:','https:','process.env','exec(','spawn(']), 'unsafe test dependency'
  assert 'node:fs' not in text or (s=='barbados' and "new URL('motion-check.json',import.meta.url)" in text), 'unreviewed filesystem use'
  (dest/name).write_bytes(b)
 p=subprocess.run(['node','--test','--test-reporter=tap',str(dest/'tests.mjs')],capture_output=True,text=True)
 (dest/'result.txt').write_text(p.stdout+p.stderr);results.append({'id':s,'exit_code':p.returncode,'passed':p.returncode==0,'scope':('Afghanistan contract assertions applied to unchanged Costa Rica motion module' if s=='costa-rica' else 'original motion unit assertions')+'; not fresh collision/source parity'})
 print(s,p.returncode,flush=True)
(R/'motion-results.json').write_text(json.dumps(results,indent=2)+'\n');assert len(results)==26 and all(x['passed'] for x in results)
