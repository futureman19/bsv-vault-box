import json, pathlib, subprocess
root=pathlib.Path(__file__).resolve().parents[2]
out=root/'evidence/security'
commands=json.loads((root/'evidence/contracts/recovery-run/commands.json').read_text())
results=[]
for item in commands:
 args=[a.replace('t_4bd2681c','t_31e30c41') for a in item['command']]
 cwd=root/'vault' if item['cwd'].endswith('vault') else root
 r=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
 (out/(item['name']+'.txt')).write_bytes(r.stdout)
 results.append(dict(name=item['name'],command=args,cwd=str(cwd),exitCode=r.returncode))
 print(item['name'],r.returncode,r.stdout.decode(errors='replace')[-500:],flush=True)
(out/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(x['exitCode']==0 for x in results)
