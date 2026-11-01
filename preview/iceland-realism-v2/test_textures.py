"""Portable texture contract: actual encoded files, not Blender-only nodes."""
from pathlib import Path
import numpy as np,json
from PIL import Image
R=Path(__file__).resolve().parent
results=[]
for family,size in [('basalt',2048),('lid',2048),('brass',2048),('interior',1024)]:
 for kind in ['color','normal','rough']:
  p=R/'textures'/f'{family}-{kind}.png';assert p.exists(),f'Missing portable map: {p.name}'
  im=Image.open(p);a=np.array(im);assert im.size==(size,size)
  assert np.isfinite(a).all()
  if kind=='normal':
   assert a[:,:,0].std()>1 and a[:,:,1].std()>1
   assert a[:,:,2].mean()>220
  elif kind=='rough':assert a.std()>3
  else:assert a.std()>3
  results.append({'file':p.name,'size':im.size,'bytes':p.stat().st_size,'std':float(a.std())})
(R/'texture-check.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
