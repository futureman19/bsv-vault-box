from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
for name,cmd in [('build',[sys.executable,str(R/'build.py')])]+[(n,[B,'--background','--factory-startup','--python-exit-code','1','--python',str(R/(n+'.py'))]) for n in ['verify_source','verify_parity','test_theme']]+[(n,[sys.executable,str(R/(n+'.py'))]) for n in ['verify_browser','verify_extended']]:
 with (R/(name+'-output.txt')).open('w') as f:
  p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 print(name,'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:sys.exit(p.returncode)
print('HTML_BYTES',(R/'the-moon-v1.html').stat().st_size,'GLB_BYTES',(R/'the-moon.glb').stat().st_size)
