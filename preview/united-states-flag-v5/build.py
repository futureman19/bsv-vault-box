from pathlib import Path
from PIL import Image
import base64,subprocess,os
R=Path(__file__).resolve().parent
# Installed baseline toolchain is used for compilation, never for viewer runtime.
deps=R/'node_modules'
if not deps.exists():deps=R.parent/'iceland-pilot/node_modules'
esbuild=deps/'esbuild/bin/esbuild'
env=dict(os.environ);env['NODE_PATH']=str(deps)
subprocess.run(['C:/Program Files/nodejs/node.exe',str(esbuild),str(R/'viewer.js'),'--bundle','--minify','--format=iife','--outfile='+str(R/'viewer.bundle.js')],env=env,check=True)
if not (R/'poster.jpg').exists():Image.open(R/'blender-source-no-fx.png').convert('RGB').save(R/'poster.jpg',quality=90,optimize=True)
html=(R/'template.html').read_text(encoding='utf8').replace('data:image/png','data:image/jpeg').replace('{{POSTER}}',base64.b64encode((R/'poster.jpg').read_bytes()).decode()).replace('{{GLB}}',base64.b64encode((R/'united-states.glb').read_bytes()).decode()).replace('{{BUNDLE}}',(R/'viewer.bundle.js').read_text().replace('</script','<\\/script'))
p=R/'united-states-flag-v5.html';p.write_text(html,encoding='utf8');assert p.stat().st_size<5_000_000;print('HTML_BYTES',p.stat().st_size,'GLB_BYTES',(R/'united-states.glb').stat().st_size)
