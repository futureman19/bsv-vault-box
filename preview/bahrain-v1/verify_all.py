"""Bounded acceptance runner; all subprocesses run for real, failures stop delivery."""
from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parent
BLENDER='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
b=[BLENDER,'--background','--factory-startup','--python-exit-code','1','--python']
checks=[]
def run(name,cmd,expected=0):
 p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
 (R/(name+'-output.txt')).write_bytes(p.stdout)
 assert p.returncode==expected,(name,p.returncode,p.stdout.decode(errors='replace')[-2000:])
 checks.append({'name':name,'status':'PASS','exit_code':p.returncode,'expected_exit_code':expected,'command':cmd})
 print(name.upper()+' PASS',flush=True)
run('motion',['node','--test','tests.mjs'])
run('source',b+['verify_source.py'])
run('parity',b+['verify_parity.py'])
run('theme',b+['verify_theme.py'])
run('negative-theme',b+['verify_theme.py','--','--negative'],1)
assert b'Ornament escaped lid hierarchy' in (R/'negative-theme-output.txt').read_bytes()
run('build',[sys.executable,'build.py'])
run('browser',[sys.executable,'verify_browser.py'])
run('extended',[sys.executable,'verify_extended.py'])
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2))
print('ALL ACCEPTANCE CHECKS PASS')
