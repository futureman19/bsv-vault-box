import subprocess, json, pathlib, hashlib
root=pathlib.Path(__file__).resolve().parents[2]
out=root/'evidence/contracts'
commands=[('vm-final',['node','node_modules/mocha/bin/mocha','--no-config','tests/ordinal-pair.test.js','tests/ordinal-sponsored.test.js','tests/native-custody.test.js','tests/launch-record.test.js'],root/'vault'),('mint-verified',['node','mint/test/run.js'],root),('typecheck',['node','node_modules/typescript/bin/tsc','--noEmit'],root/'vault'),('pair-vectors',['node','scripts/ordinal-pair-vectors.js'],root/'vault'),('sponsor-vectors',['node','scripts/ordinal-sponsored-vectors.js'],root/'vault'),('proof-verified',['node','evidence/contracts/replay-proof.js','evidence/contracts/proof.json','evidence/contracts/fixture-trusted-policy.json'],root),('recovery-cli',['node','mint/scripts/recovery-inspect.js',str(out/'fixture-sales.jsonl'),str(out/'fixture-pool.jsonl'),str(out/'fixture-observations.json'),'box-1','02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5','2'],root)]
results=[]
for name,args,cwd in commands:
 r=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
 (out/(name+'.txt')).write_bytes(r.stdout)
 results.append(dict(name=name,command=args,cwd=str(cwd),exitCode=r.returncode))
 print(name,r.returncode,r.stdout.decode(errors='replace')[-450:])
(out/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(x['exitCode']==0 for x in results)
