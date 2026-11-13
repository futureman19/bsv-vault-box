from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parent
B=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
def run(args,log):
 p=subprocess.run(args,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/log).write_bytes(p.stdout);print(p.stdout.decode('utf8',errors='replace'));assert p.returncode==0,(args,p.returncode)
run([sys.executable,'build.py'],'build-output.txt')
run(['node','--test','tests.mjs'],'motion-output.txt')
for script,label in [('verify_source.py','source'),('verify_parity.py','parity'),('verify_theme.py','theme')]:
 run([B,'--background','--factory-startup','--python-exit-code','1','--python',str(R/script)],label+'-output.txt');print(label.upper()+' PASS')
for script,label in [('verify_browser.py','browser'),('verify_extended.py','extended')]:
 run([sys.executable,script],label+'-output.txt');print(label.upper()+' PASS')
run([sys.executable,'package_delivery.py'],'package-output.txt')
print('ALL CHECKS PASS')
