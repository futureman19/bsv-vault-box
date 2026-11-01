import subprocess, base64, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
node=shutil.which('node')

subprocess.run([str(ROOT/'node_modules/@esbuild/win32-x64/esbuild.exe'),str(ROOT/'viewer.js'),'--bundle','--minify','--format=iife','--outfile='+str(ROOT/'viewer.bundle.js')],check=True)
html=(ROOT/'template.html').read_text(encoding='utf8').replace('{{POSTER}}',base64.b64encode((ROOT/'poster.png').read_bytes()).decode()).replace('{{GLB}}',base64.b64encode((ROOT/'iceland.glb').read_bytes()).decode()).replace('{{BUNDLE}}',(ROOT/'viewer.bundle.js').read_text().replace('</script','<\\/script'))
(ROOT/'iceland-pilot.html').write_text(html,encoding='utf8')
shutil.copyfile(ROOT/'node_modules/three/LICENSE',ROOT/'THREE-LICENSE.txt')
print('Built offline HTML:',(ROOT/'iceland-pilot.html').stat().st_size)
