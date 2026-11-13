from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parent
blender='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
node='C:/Program Files/nodejs/node.exe'
commands=[[sys.executable,str(R/'build.py')],[node,str(R/'test_motion.mjs')]]
commands += [[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/(s+'.py'))] for s in ['verify_source','verify_parity','verify_theme_source']]
commands += [[sys.executable,str(R/(s+'.py'))] for s in ['verify_browser','verify_extended']]
results=[]
for i,c in enumerate(commands):
 p=subprocess.run(c,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/('verification-'+str(i)+'.txt')).write_bytes(p.stdout)
 results.append({'command':c,'exit_code':p.returncode})
 print('PASS' if p.returncode==0 else 'FAIL',Path(c[-1]).name,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','commands':results},indent=2))
print('ALL ACCEPTANCE CHECKS PASS')
