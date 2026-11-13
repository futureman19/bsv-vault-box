from pathlib import Path
import os,subprocess,sys,json
R=Path(__file__).resolve().parent
B=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[[sys.executable,'build.py'],['node','--test','tests.mjs']]+[[B,'--background','--factory-startup','--python-exit-code','1','--python',str(R/f)] for f in ['verify_source.py','verify_parity.py','verify_theme.py']]+[[sys.executable,f] for f in ['verify_browser.py','verify_extended.py']]
results=[]
for i,cmd in enumerate(commands):
 p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace',timeout=600)
 (R/f'verification-{i}.txt').write_text(p.stdout,encoding='utf8');print(p.stdout);results.append({'command':cmd,'exit_code':p.returncode});assert p.returncode==0,cmd
(R/'verification-check.json').write_text(json.dumps({'status':'PASS','commands':results},indent=2));print('ALL_CHECKS_PASS')
