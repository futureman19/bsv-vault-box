from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
commands=[('build',[sys.executable,str(R/'build.py')])]+[(n,[B,'-b','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+n+'.py'))]) for n in ['source','parity','theme']]+[(n,[sys.executable,str(R/('verify_'+n+'.py'))]) for n in ['browser','extended']]
for n,c in commands:
 p=subprocess.run(c,capture_output=True);(R/(n+'-output.txt')).write_bytes(p.stdout+p.stderr);print(n,'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:sys.exit(p.returncode)
p=subprocess.run([B,'-b','--factory-startup','--python-exit-code','1','--python',str(R/'verify_theme.py'),'--','--negative'],capture_output=True);(R/'initial/detached-ornament-negative.txt').write_bytes(p.stdout+p.stderr);assert p.returncode!=0 and b'Detached ornament rejected' in p.stdout+p.stderr
print('negative-control PASS',flush=True)
