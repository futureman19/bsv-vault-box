import json, pathlib, subprocess, sys
root=pathlib.Path(__file__).resolve().parents[2]
out=root/'evidence/security-fix'
mode=sys.argv[1] if len(sys.argv)>1 else 'green'
commands=json.loads((root/'evidence/contracts/recovery-run/commands.json').read_text())
if mode=='red': commands=[commands[1]]
commands.append(dict(name='challenges',command=['node','--test','evidence/security/challenges.test.js'],cwd=str(root)))
results=[]
for item in commands:
 args=[a.replace('t_4bd2681c','t_d2ef3c5c') for a in item['command']]
 cwd=root/'vault' if item['cwd'].endswith('vault') else root
 r=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
 (out/(item['name']+'-'+mode+'.txt')).write_bytes(r.stdout)
 results.append(dict(name=item['name'],command=args,cwd=str(cwd),exitCode=r.returncode))
 print(item['name'],r.returncode,r.stdout.decode(errors='replace')[-650:],flush=True)
(out/('commands-'+mode+'.json')).write_text(json.dumps(results,indent=2)+'\n')
if mode!='red': assert all(x['exitCode']==0 for x in results)
