from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,str(R/'build.py')])]+[(n,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/(n+'.py'))]) for n in ['verify_source','verify_parity','verify_theme']]+[(n,[sys.executable,str(R/(n+'.py'))]) for n in ['verify_browser','verify_extended']]
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(R/(name+'-final-output.txt')).write_text(p.stdout,encoding='utf8');print(name,'PASS' if p.returncode==0 else 'FAIL',flush=True);assert p.returncode==0,p.stdout;results.append({'check':name,'status':'PASS','exit_code':p.returncode})
(R/'acceptance.json').write_text(json.dumps(results,indent=2));print('HTML_BYTES',(R/'peru-v1.html').stat().st_size,'GLB_BYTES',(R/'peru.glb').stat().st_size)
