import pathlib,json,subprocess,shutil
R=pathlib.Path(__file__).resolve().parent
ids=json.loads((R/'assigned.json').read_text()); es=json.loads((R/'parent-ledger.json').read_text())['entries']; results=[]
node=shutil.which('node.exe') or shutil.which('node')
for e in es:
 if e['id'] not in ids:continue
 s=e['id']; dest=R/'motion'/s;dest.mkdir(parents=True,exist_ok=True); base=str(pathlib.PurePosixPath(e['viewer']['path']).parent); commit=e['selection']['commit']
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,base]).decode().splitlines()
 test=next((n for n in ['tests.mjs','test_motion.mjs'] if base+'/'+n in paths),None)
 for name in ['motion.mjs','tests.mjs']:
  source=(base+'/'+('motion.mjs' if name=='motion.mjs' else test)) if name=='motion.mjs' or test else 'preview/algeria-v1/tests.mjs'
  ref=commit if name=='motion.mjs' or test else next(x['selection']['commit'] for x in es if x['id']=='algeria')
  b=subprocess.check_output(['git','show',ref+':'+source]); text=b.decode()
  assert not any(t in text for t in ['child_process','fetch(','http:','https:','process.env','exec(','spawn(']), 'unsafe test dependency'
  assert 'node:fs' not in text or any(x in text for x in ["new URL('motion-check.json',import.meta.url)", "new URL('./motion-check.json',import.meta.url)"]), 'unreviewed filesystem use'
  if 'motion-check.json' in text and base+'/motion-check.json' in paths:
   (dest/'motion-check.json').write_bytes(subprocess.check_output(['git','show',commit+':'+base+'/motion-check.json']))
  (dest/name).write_bytes(b)
 p=subprocess.run([node,'--test','--test-reporter=tap',str(dest/'tests.mjs')],capture_output=True,text=True)
 (dest/'result.txt').write_text(p.stdout+p.stderr);results.append({'id':s,'exit_code':p.returncode,'passed':p.returncode==0,'scope':('original motion unit assertions' if test else 'Reused Algeria contract assertions applied to unchanged selected motion module')+'; not fresh collision/source parity'})
 print(s,p.returncode,flush=True)
(R/'motion-results.json').write_text(json.dumps(results,indent=2)+'\n');assert len(results)==25 and all(x['passed'] for x in results)
