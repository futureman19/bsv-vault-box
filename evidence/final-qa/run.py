"""Independent bounded final QA; no chain launch or production mutations."""
from pathlib import Path
import subprocess, sys, os, json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'evidence/final-qa'
gates=[
('install',['npm','ci','--ignore-scripts','--no-audit','--no-fund'],ROOT/'vault'),
('allocation',[sys.executable,'launch/mint/test_dry_run.py'],ROOT),
('collection',[sys.executable,'launch/collection/test_consolidation.py'],ROOT),
('assets',[sys.executable,'launch/assets/test_packaging.py'],ROOT),
('ops-unit',[sys.executable,'launch/ops/test_recovery.py'],ROOT),
('ops-drill',[sys.executable,'launch/ops/exercise.py','--output','evidence/final-qa/ops-drill'],ROOT),
('vm',['node','node_modules/mocha/bin/mocha','--no-config','tests/ordinal-pair.test.js','tests/ordinal-sponsored.test.js','tests/native-custody.test.js','tests/launch-record.test.js'],ROOT/'vault'),
('mint-posix',['node','mint/test/run.js'],ROOT),
('security',['node','--test','evidence/security/challenges.test.js'],ROOT),
('typecheck',['node','node_modules/typescript/bin/tsc','--noEmit'],ROOT/'vault'),
('proof',['node','evidence/contracts/replay-proof.js','evidence/contracts/proof.json','evidence/contracts/fixture-trusted-policy.json'],ROOT),
('historical-node-replay',['node','evidence/rehearsal/audit-regtest.js','evidence/rehearsal/regtest'],ROOT),
('claw-unit',['node','--test','test/claw-interactive.test.js'],ROOT),
('web',[sys.executable,'test/web-launch-browser.py'],ROOT),
('claw',[sys.executable,'test/claw-launch-browser.py'],ROOT)]
results=[]
for name,cmd,cwd in gates:
 if name=='install' and os.name=='nt': cmd[0]='npm.cmd'
 with (OUT/(name+'.txt')).open('w',encoding='utf8') as log:
  p=subprocess.run(cmd,cwd=cwd,env=dict(os.environ,BOXSV_EVIDENCE_DIR='evidence/final-qa/'+name),stdout=log,stderr=subprocess.STDOUT,timeout=600)
 results.append(dict(name=name,command=cmd,cwd=str(cwd),exitCode=p.returncode))
 (OUT/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,p.returncode,flush=True)
sys.exit(any(r['exitCode'] for r in results))
