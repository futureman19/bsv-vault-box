"""Build and rerun bounded acceptance; does not regenerate the authored source."""
from pathlib import Path
import os,subprocess,sys
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
for f in ['verify_theme.py','verify_source.py','verify_parity.py']:
 p=subprocess.run([blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/f)],capture_output=True,text=True)
 (R/(f.removesuffix('.py')+'-output.txt')).write_text(p.stdout+p.stderr,encoding='utf8');p.check_returncode();print(f+' PASS',flush=True)
for cmd in [['node','--test',str(R/'tests.mjs')],[sys.executable,str(R/'build.py')],[sys.executable,str(R/'verify_browser.py')],[sys.executable,str(R/'verify_extended.py')]]:
 subprocess.run(cmd,check=True)
print('SOURCE PARITY THEME MOTION BUILD BROWSER EXTENDED PASS')
