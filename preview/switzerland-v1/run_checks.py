from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parent
blender='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
commands=[['node','--test',str(R/'tests.mjs')],[sys.executable,str(R/'build.py')]]
commands += [[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/n)] for n in ['verify_source.py','verify_parity.py','verify_theme.py']]
commands += [[sys.executable,str(R/n)] for n in ['verify_browser.py','verify_extended.py']]
results=[]
for i,cmd in enumerate(commands):
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 name='check-'+str(i)+'.txt';(R/name).write_text(p.stdout)
 print(p.stdout,flush=True);results.append({'command':cmd,'exit_code':p.returncode,'log':name})
 (R/'run-checks.json').write_text(json.dumps(results,indent=2))
 if p.returncode:sys.exit(p.returncode)
print('ALL CHECKS PASS')
