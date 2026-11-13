"""Build, reopen and independently exercise the delivered asset. Does not author."""
from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER_EXE','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,str(R/'build.py')])]
commands += [(n,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/(n+'.py'))]) for n in ['verify_source','verify_parity','verify_theme_source']]
commands += [('motion',['C:/Program Files/nodejs/node.exe',str(R/'tests.mjs')])]
commands += [(n,[sys.executable,str(R/(n+'.py'))]) for n in ['verify_browser','verify_extended']]
for n,cmd in commands:
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(n+'-output.txt')).write_bytes(p.stdout)
 if p.returncode:print(p.stdout.decode(errors='replace'));raise SystemExit(p.returncode)
 print(n+' PASS',flush=True)
print('HTML_BYTES',(R/'mali-v1.html').stat().st_size,'GLB_BYTES',(R/'mali.glb').stat().st_size)
