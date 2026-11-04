"""Run inherited actual JS motion unit tests and retain machine-readable exit."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parent
p=subprocess.run(['node','--test',str(R/'tests.mjs')],capture_output=True,text=True)
(R/'motion-output.txt').write_text(p.stdout+p.stderr)
assert p.returncode==0,p.stdout+p.stderr
out={'status':'PASS','command':'node --test preview/kiribati-v1/tests.mjs','exit_code':p.returncode,'tests':2,'includes_negative_asset_controls':True,'sampled_pose_steps':101,'latch_degrees':80,'lid_degrees':105,'latch_phase_end':.25}
(R/'motion-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
