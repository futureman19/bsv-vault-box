import pathlib,json,subprocess,hashlib,shutil
R=pathlib.Path(__file__).resolve().parent
rows=json.loads((R/'packaging-results.json').read_text());out=[]
node=shutil.which('node.exe') or shutil.which('node')
for e in rows:
 p=R/'motion'/e['id'];p.mkdir(parents=True,exist_ok=True);records=[]
 for n in ['tests.mjs','motion.mjs']:
  src=str(pathlib.PurePosixPath(e['viewer']['path']).parent/n)
  commit=e['selection']['commit']
  if n=='tests.mjs':
   src='preview/albania-v1/tests.mjs';commit='3e0daf79c8bf96da31c14d0bdfeb17f16e9a053a'
  b=subprocess.check_output(['git','show',commit+':'+src]);(p/n).write_bytes(b);records.append({'path':src,'commit':commit,'sha256':hashlib.sha256(b).hexdigest()})
 run=subprocess.run([node,'--test','--test-reporter=tap',str(p/'tests.mjs')],capture_output=True)
 (p/'output.txt').write_bytes(run.stdout+run.stderr)
 out.append({'id':e['id'],'exit_code':run.returncode,'source':records,'scope':'shared Albania endpoint tests against each immutable motion module; not collision sampling'})
 assert run.returncode==0
(R/'motion-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',len(out),'shared endpoint suites against original motion modules; not original per-asset test suites or collision sampling')
