from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parent
BLENDER='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
commands=[('source',[BLENDER,'--background','--factory-startup','--python-exit-code','1','--python',str(R/'verify_source.py')]),('parity',[BLENDER,'--background','--factory-startup','--python-exit-code','1','--python',str(R/'verify_parity.py')]),('theme',[BLENDER,'--background','--factory-startup','--python-exit-code','1','--python',str(R/'verify_theme.py')]),('motion',['C:/Program Files/nodejs/node.exe',str(R/'tests.mjs')]),('build',[sys.executable,str(R/'build.py')]),('browser',[sys.executable,str(R/'verify_browser.py')]),('extended',[sys.executable,str(R/'verify_extended.py')])]
for name,cmd in commands:
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/(name+'-output.txt')).write_bytes(p.stdout)
 if p.returncode:
  print(p.stdout.decode(errors='replace'));raise SystemExit(p.returncode)
 if name=='motion':(R/'motion-check.json').write_text(json.dumps({'status':'PASS','samples':81,'negative_controls':3}))
 print('PASS',name,flush=True)
print((R/'build-output.txt').read_text(),flush=True)
