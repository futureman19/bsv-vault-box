from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe');node=os.environ.get('NODE','C:/Program Files/nodejs/node.exe')
def run(name,args):
 p=subprocess.run(args,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/(name+'-log.txt')).write_bytes(p.stdout)
 if p.returncode:print(p.stdout.decode(errors='replace'));raise SystemExit(p.returncode)
 print(name.upper()+'_PASS')
for s in ['verify_source','verify_parity','verify_theme']:run(s,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/(s+'.py'))])
run('motion',[node,'--test',str(R/'tests.mjs')]);run('build',[sys.executable,str(R/'build.py')]);print((R/'build-log.txt').read_text())
for s,n in [('verify_browser','browser'),('verify_extended','extended')]:run(n,[sys.executable,str(R/(s+'.py'))])
run('delivery',[sys.executable,str(R/'package_delivery.py')]);print('ALL_ACCEPTANCE_CHECKS_PASS')
