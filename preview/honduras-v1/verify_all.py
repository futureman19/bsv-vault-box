from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
for name in ['build','verify_source','verify_parity','verify_theme','verify_browser','verify_extended']:
 cmd=([blender,'--background','--factory-startup','--python-exit-code','1','--python'] if name in ['verify_source','verify_parity','verify_theme'] else [sys.executable])+[str(R/(name+'.py'))]
 result=subprocess.run(cmd,capture_output=True)
 (R/(name+'-rerun.txt')).write_bytes(result.stdout+result.stderr)
 if result.returncode:print((result.stdout+result.stderr).decode('utf8',errors='replace'));raise SystemExit(result.returncode)
 print(name+' PASS',flush=True)
print('ALL ACCEPTANCE CHECKS PASS')
