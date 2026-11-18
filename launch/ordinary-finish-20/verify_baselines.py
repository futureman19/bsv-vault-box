"""Run same explicitly shared interaction contract against unchanged baselines."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parent; REPO=R.parents[1]
base=(REPO/'preview/bangladesh-finish-v2/verify_browser.py').read_text()
rows=[]
for row in json.loads((R/'baseline.json').read_text()):
 D=R/'runtime'/row['id'];D.mkdir(parents=True,exist_ok=True)
 text=base.replace("URL=(R/'bangladesh-finish-v2.html').as_uri()",'URL='+repr((REPO/row['viewer']).as_uri()))
 text=text.replace(",('mobile-dpr2',390,844,2),('mobile-dpr3',390,844,3)","")
 text=text.replace("assert p.evaluate('pilot.renderer.getPixelRatio()')==2","assert p.evaluate('pilot.renderer.getPixelRatio()')==min(dpr,2)")
 text=text.replace("'drawing_ratio':2","'drawing_ratio':min(dpr,2)")
 (D/'shared_contract.py').write_text(text)
 result=subprocess.run([sys.executable,str(D/'shared_contract.py')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (D/'output.txt').write_bytes(result.stdout)
 rows.append({'id':row['id'],'exit_code':result.returncode,'shared_contract':'Bangladesh renderer-independent interaction assertions; no fresh source/collision claim','results':str((D/'browser-check.json').relative_to(REPO))})
 (R/'runtime-summary.json').write_text(json.dumps(rows,indent=2));print(row['id'],result.returncode,flush=True)
assert len(rows)==20 and all(r['exit_code']==0 for r in rows)
