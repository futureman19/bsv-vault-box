from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',['C:/Program Files/nodejs/node.exe','--test',str(R/'tests.mjs')])]+[(x,[B,'--background','--factory-startup','--python-exit-code','1','--python',str(R/(x+'.py'))]) for x in ['verify_source','verify_parity','verify_theme']]+[(x,[sys.executable,str(R/(x+'.py'))]) for x in ['verify_browser','verify_extended']]
for name,cmd in commands:
 p=subprocess.run(cmd,capture_output=True,text=True);(R/(name+'-output.txt')).write_text(p.stdout+p.stderr,encoding='utf8');assert p.returncode==0,(name,p.stdout[-1500:],p.stderr[-1500:]);print(name.upper()+' PASS',flush=True)
print('HTML_BYTES='+str((R/'southern-ocean-v1.html').stat().st_size));print('GLB_BYTES='+str((R/'southern-ocean.glb').stat().st_size))
