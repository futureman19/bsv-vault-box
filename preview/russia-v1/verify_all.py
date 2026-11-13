from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
for script in ['verify_source.py','verify_parity.py','verify_theme.py']:
 p=subprocess.run([B,'--background','--factory-startup','--python-exit-code','1','--python',str(R/script)],capture_output=True)
 (R/(script+'.log')).write_bytes(p.stdout+p.stderr);assert p.returncode==0,script
 print(script,'PASS',flush=True)
for cmd in [[sys.executable,str(R/'build.py')],['node','--test',str(R/'tests.mjs')],[sys.executable,str(R/'verify_browser.py')],[sys.executable,str(R/'verify_extended.py')]]:
 p=subprocess.run(cmd,capture_output=True);(R/(Path(cmd[-1]).name+'.log')).write_bytes(p.stdout+p.stderr);assert p.returncode==0,cmd
 print(Path(cmd[-1]).name,'PASS',flush=True)
 if cmd[-1].endswith('build.py'):print(p.stdout.decode(),flush=True)
print('ALL ACCEPTANCE CHECKS PASS')
