from pathlib import Path
from PIL import Image
import base64,subprocess,os
R=Path(__file__).resolve().parent
# Geometry-only repair: preserve the exact already-compiled immutable runtime.
assert (R/'viewer.bundle.js').read_bytes()==(R/'historical-v1/viewer.bundle.js').read_bytes()
Image.open(R/'poster.png').convert('RGB').save(R/'poster.jpg',quality=90,optimize=True)
html=(R/'template.html').read_text(encoding='utf8').replace('data:image/png','data:image/jpeg').replace('{{POSTER}}',base64.b64encode((R/'poster.jpg').read_bytes()).decode()).replace('{{GLB}}',base64.b64encode((R/'venezuela.glb').read_bytes()).decode()).replace('{{BUNDLE}}',(R/'viewer.bundle.js').read_text().replace('</script','<\\/script'))
p=R/'venezuela-repair-v2.html';p.write_text(html,encoding='utf8');assert p.stat().st_size<5_000_000;print('HTML_BYTES',p.stat().st_size,'GLB_BYTES',(R/'venezuela.glb').stat().st_size)
