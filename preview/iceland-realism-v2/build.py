import subprocess, base64, shutil, os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DEPS=ROOT/'node_modules'
if not DEPS.exists():DEPS=ROOT/'../iceland-pilot/node_modules'
os.environ['NODE_PATH']=str(DEPS.resolve())
node=shutil.which('node')

subprocess.run([str(DEPS/'@esbuild/win32-x64/esbuild.exe'),str(ROOT/'viewer.js'),'--bundle','--minify','--format=iife','--outfile='+str(ROOT/'viewer.bundle.js')],check=True)
html=(ROOT/'template.html').read_text(encoding='utf8').replace('{{POSTER}}',base64.b64encode((ROOT/'poster.png').read_bytes()).decode()).replace('{{GLB}}',base64.b64encode((ROOT/'iceland.glb').read_bytes()).decode()).replace('{{BUNDLE}}',(ROOT/'viewer.bundle.js').read_text().replace('</script','<\\/script'))
(ROOT/'iceland-realism-v2.html').write_text(html,encoding='utf8')
shutil.copyfile(DEPS/'three/LICENSE',ROOT/'THREE-LICENSE.txt')
print('Built offline HTML:',(ROOT/'iceland-realism-v2.html').stat().st_size)
