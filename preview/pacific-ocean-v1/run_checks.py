"""Run bounded acceptance from any working directory; no authoring or chain activity."""
from pathlib import Path
import subprocess,sys,json
from PIL import Image
R=Path(__file__).resolve().parent
BLENDER='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
def run(label,args):
 p=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace')
 (R/(label+'-output.txt')).write_text(p.stdout+p.stderr,encoding='utf8')
 print(label.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:print(p.stdout+p.stderr);raise SystemExit(p.returncode)
for name in ['source','parity','theme']:
 run(name,[BLENDER,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+name+'.py'))])
im=Image.open(R/'poster.png').convert('RGBA');assert im.width>=800 and im.height>=700
import numpy as np
px=np.array(im);assert (px[:,:,3]>0).mean()>.5 and px[:,:,:3].max()>100 and px[:,:,:3].std()>10
run('build',[sys.executable,str(R/'build.py')]);print((R/'build-output.txt').read_text(),flush=True)
run('motion',['C:/Program Files/nodejs/node.exe','--test',str(R/'tests.mjs')])
run('browser',[sys.executable,str(R/'verify_browser.py')])
run('extended',[sys.executable,str(R/'verify_extended.py')])
print('ALL ACCEPTANCE CHECKS PASS',flush=True)
