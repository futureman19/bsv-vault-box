"""Bounded final verification. Never invokes wallet, chain or network services."""
from pathlib import Path
import subprocess,sys,json,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
checks=[]
def run(name,args,expected=0):
 p=subprocess.run(args,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(name+'-output.txt')).write_bytes(p.stdout)
 assert p.returncode==expected,(name,p.returncode,p.stdout.decode(errors='replace')[-1500:])
 checks.append({'name':name,'exit_code':p.returncode,'expected_exit_code':expected,'status':'PASS'})
 print(name,'PASS','exit='+str(p.returncode),flush=True)
run('build',[sys.executable,'build.py'])
run('motion',['node','--test','tests.mjs'])
for name in ['source','parity','theme']:
 run(name,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+name+'.py'))])
run('theme-negative',[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/'verify_theme.py'),'--','--negative-control'],1)
run('browser',[sys.executable,'verify_browser.py'])
run('extended',[sys.executable,'verify_extended.py'])
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':checks,'negative_control':'Post-implementation in-memory detachment of mountain from lid is rejected; saved source is never modified.'},indent=2))
print('ALL ACCEPTANCE CHECKS PASS')
