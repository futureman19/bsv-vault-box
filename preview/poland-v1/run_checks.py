from pathlib import Path
import subprocess,os,sys
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
for script in ['verify_source.py','verify_parity.py','verify_design.py','build.py','verify_browser.py','verify_theme.py']:
 cmd=([blender,'--background','--factory-startup','--python-exit-code','1','--python'] if script.startswith(('verify_source','verify_parity','verify_design')) else [sys.executable])+[str(R/script)]
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/(script[:-3]+'-run.txt')).write_bytes(p.stdout);print(script,'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:raise SystemExit(p.returncode)
p=subprocess.run(['node','--test',str(R/'tests.mjs')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/'motion-output.txt').write_bytes(p.stdout);assert p.returncode==0
print('motion PASS');print('ALL CHECKS PASS')
