"""Canonical bounded verification; does not regenerate authoring."""
from pathlib import Path
import subprocess,sys,json,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,'build.py']),('motion',['node','--test','tests.mjs'])]
commands += [(name,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/script)]) for name,script in [('source','verify_source.py'),('parity','verify_parity.py'),('theme-source','verify_theme_source.py')]]
commands += [(name,[sys.executable,script]) for name,script in [('browser','verify_browser.py'),('extended','verify_extended.py'),('theme','test_theme.py')]]
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace');(R/(name+'-output.txt')).write_text(p.stdout+p.stderr,encoding='utf8')
 results.append({'check':name,'command':cmd,'exit_code':p.returncode,'status':'PASS' if p.returncode==0 else 'FAIL'})
 (R/'checks.json').write_text(json.dumps(results,indent=2));print(name.upper(),results[-1]['status'],flush=True)
 if name=='build':print(p.stdout.strip(),flush=True)
 if p.returncode:print(p.stdout,p.stderr);sys.exit(p.returncode)
print('ALL ACCEPTANCE CHECKS PASS')
