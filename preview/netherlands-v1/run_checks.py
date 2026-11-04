from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',['node','--test',str(R/'tests.mjs')])]
commands += [(name,[B,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+name+'.py'))]) for name in ['source','theme','parity']]
commands += [(name,[sys.executable,str(R/('verify_'+name+'.py'))]) for name in ['browser','extended']]
for name,cmd in commands:
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(name+'-output.txt')).write_bytes(p.stdout)
 print(name.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:print(p.stdout.decode('utf8',errors='replace'));sys.exit(p.returncode)
print('ALL ACCEPTANCE CHECKS PASS')
