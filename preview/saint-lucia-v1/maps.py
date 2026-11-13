from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1161);y,x=np.mgrid[0:256,0:256]
f=np.sin(x*.13+np.sin(y*.08)*2)*3+np.sin(y*.17+x*.07)*3+rng.normal(0,5,(256,256))
for name,base in [('stone',(86,99,93)),('forest',(63,96,48))]:
 a=np.clip(np.array(base)[None,None,:]+f[:,:,None]*np.array([1,.9,.7]),0,255).astype('uint8');Image.fromarray(a).save(R/(name+'-color.png'))
a=np.clip(195+f*2,150,235).astype('uint8');Image.fromarray(a).convert('RGB').save(R/'stone-roughness.png')
print('MAPS_PASS 3 procedural 256x256 maps')
