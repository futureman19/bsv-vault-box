"""Run bounded integrated offline gates; retain output separately from parents."""
from pathlib import Path
import subprocess, json, os, sys
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'evidence/rehearsal'
gates=[
 ('allocation',[sys.executable,'launch/mint/test_dry_run.py'],ROOT),
 ('collection',[sys.executable,'launch/collection/test_consolidation.py'],ROOT),
 ('vm',['node','node_modules/mocha/bin/mocha','--no-config','tests/ordinal-pair.test.js','tests/ordinal-sponsored.test.js','tests/native-custody.test.js','tests/launch-record.test.js'],ROOT/'vault'),
 ('mint-posix',['node','mint/test/run.js'],ROOT),
 ('security',['node','--test','evidence/security/challenges.test.js'],ROOT),
 ('typecheck',['node','node_modules/typescript/bin/tsc','--noEmit'],ROOT/'vault'),
 ('proof',['node','evidence/contracts/replay-proof.js','evidence/contracts/proof.json','evidence/contracts/fixture-trusted-policy.json'],ROOT),
 ('claw-unit',['node','--test','test/claw-interactive.test.js'],ROOT),
 ('web',[sys.executable,'test/web-launch-browser.py'],ROOT),
 ('claw',[sys.executable,'test/claw-launch-browser.py'],ROOT),
]
results=[]
for name,cmd,cwd in gates:
 env=dict(os.environ, BOXSV_EVIDENCE_DIR='evidence/rehearsal/'+name)
 with (OUT/(name+'.txt')).open('w',encoding='utf8') as f:
  p=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600)
 results.append(dict(name=name,command=cmd,cwd=str(cwd),exitCode=p.returncode))
 (OUT/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,p.returncode,flush=True)
sys.exit(any(x['exitCode'] for x in results))
