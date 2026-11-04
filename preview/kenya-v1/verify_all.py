from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
checks=[]
p=subprocess.run(['node',str(R/'tests.mjs')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(R/'motion-output.txt').write_bytes(p.stdout)
assert p.returncode==0,p.stdout.decode(errors='replace')
print(p.stdout.decode().strip(),flush=True)
checks.append('tests.mjs')
for script in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','verify_theme.py']:
 cmd=([B,'--background','--factory-startup','--python-exit-code','1','--python'] if script in ['verify_source.py','verify_parity.py'] else [sys.executable])+[str(R/script)]
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/(script.removesuffix('.py')+'-output.txt')).write_bytes(p.stdout)
 print(script,'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:print(p.stdout.decode(errors='replace'));raise SystemExit(p.returncode)
 checks.append(script)
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2))
print('HTML_BYTES',(R/'kenya-v1.html').stat().st_size,'GLB_BYTES',(R/'kenya.glb').stat().st_size)
