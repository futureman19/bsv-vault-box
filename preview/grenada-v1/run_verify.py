from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER_EXE','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
def run(label,command,log):
 p=subprocess.run(command,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/log).write_bytes(p.stdout)
 if p.returncode:
  print(p.stdout.decode('utf8',errors='replace'));raise SystemExit(p.returncode)
 print(label+' PASS',flush=True)
run('BUILD',[sys.executable,'build.py'],'build-output.txt')
run('MOTION',['node','--test','tests.mjs'],'motion-output.txt')
for label,script in [('SOURCE','verify_source.py'),('PARITY','verify_parity.py'),('THEME','verify_theme.py')]:
 run(label,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/script)],label.lower()+'-output.txt')
run('BROWSER',[sys.executable,'verify_browser.py'],'browser-output.txt')
run('EXTENDED',[sys.executable,'verify_extended.py'],'extended-output.txt')
subprocess.run([sys.executable,'package_delivery.py'],cwd=R,check=True)
print('ALL ACCEPTANCE CHECKS PASS',flush=True)
