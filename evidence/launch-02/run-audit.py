"""Bounded offline VM/fixture gates; no node/network/key entrypoints."""
import pathlib, subprocess, shutil, json, hashlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'evidence/launch-02'
V=ROOT/'.audit-sources/bundle/vault'
node=shutil.which('node')
commands=[('vm-tests',[node,'node_modules/mocha/bin/mocha.js','--no-config','tests/ordinal-pair.test.js','tests/ordinal-sponsored.test.js','tests/native-custody.test.js','tests/four-ordinal.test.js','tests/four-ordinal-sponsored.test.js']),('pair-vectors',[node,'scripts/ordinal-pair-vectors.js']),('sponsor-vectors',[node,'scripts/ordinal-sponsored-vectors.js']),('four-vectors',[node,'scripts/four-ordinal-vectors.js']),('node-evidence-replay',[node,'scripts/four-ordinal-regtest-replay.js','../evidence/four-ordinal-sponsored/regtest-run-1']),('typecheck',[node,'node_modules/typescript/bin/tsc','--noEmit'])]
results=[]
for name,args in commands:
 r=subprocess.run(args,cwd=V,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
 (OUT/(name+'.txt')).write_bytes(r.stdout)
 results.append({'gate':name,'argv':args[1:],'cwd':'.audit-sources/bundle/vault','exit':r.returncode})
 print(name,r.returncode,flush=True)
(OUT/'gates.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['exit']==0 for r in results)
