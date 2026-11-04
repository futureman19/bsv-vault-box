from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',['node',str(R/'tests.mjs')])]
for n in ['source','parity','theme_source']:
 commands.append((n,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+n+'.py'))]))
for n in ['browser','extended']:commands.append((n,[sys.executable,str(R/('verify_'+n+'.py'))]))
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace');(R/(name+'-output.txt')).write_text(p.stdout+p.stderr,encoding='utf8');print(name.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True);results.append({'check':name,'exit_code':p.returncode});assert p.returncode==0,p.stdout+p.stderr
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':results},indent=2))
print('HTML_BYTES', (R/'dominica-v1.html').stat().st_size,'GLB_BYTES',(R/'dominica.glb').stat().st_size)
