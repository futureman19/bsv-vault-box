from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
node='C:/Program Files/nodejs/node.exe'
def run(cmd,log):
 p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/log).write_bytes(p.stdout);print(p.stdout.decode(errors='replace'));assert p.returncode==0,(cmd,p.returncode)
run([sys.executable,'build.py'],'build-output.txt')
run([node,'--test','tests.mjs'],'motion-output.txt')
for test in ['source','parity','theme']:
 run([blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+test+'.py'))],test+'-output.txt')
for test in ['browser','extended']:
 run([sys.executable,'verify_'+test+'.py'],test+'-output.txt')
subprocess.run([sys.executable,str(R/'package_delivery.py')],check=True)
print('ALL ACCEPTANCE CHECKS PASS')
