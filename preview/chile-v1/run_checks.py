from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',['node',str(R/'test_motion.mjs')])]
commands += [(n,[B,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+n+'.py'))]) for n in ['source','parity','theme']]
commands += [(n,[sys.executable,str(R/('verify_'+n+'.py'))]) for n in ['browser','extended']]
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,capture_output=True,text=True,errors='replace',timeout=600)
 (R/(name+'-output.txt')).write_text(p.stdout+p.stderr,encoding='utf8')
 print(name.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 results.append({'check':name,'exit_code':p.returncode})
 if p.returncode:print(p.stdout+p.stderr);raise SystemExit(p.returncode)
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','owner':'Hermes direct execution; no Codex changes accepted','checks':results},indent=2))
print('ALL ACCEPTANCE CHECKS PASS')
