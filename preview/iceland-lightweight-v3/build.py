"""Embed complete runtime, model and actual source render. No network dependencies."""
from pathlib import Path
from PIL import Image
import base64
R=Path(__file__).resolve().parent
Image.open(R/'poster.png').convert('RGB').save(R/'poster.jpg',quality=92,subsampling=0,optimize=True)
html=(R/'template.html').read_text(encoding='utf8').replace('data:image/png','data:image/jpeg').replace('{{POSTER}}',base64.b64encode((R/'poster.jpg').read_bytes()).decode()).replace('{{GLB}}',base64.b64encode((R/'iceland.glb').read_bytes()).decode()).replace('{{BUNDLE}}',(R/'viewer.bundle.js').read_text().replace('</script','<\\/script'))
html=html.replace('Iceland / Basalt','Iceland / Basalt · Lightweight v3')
p=R/'iceland-lightweight-v3.html';p.write_text(html,encoding='utf8');assert p.stat().st_size<=5_000_000;print(p.stat().st_size)
