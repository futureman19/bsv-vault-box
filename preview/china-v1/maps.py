from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:256,0:256];rng=np.random.default_rng(82)
v=.5+.12*np.sin(x*.10+y*.13)*np.cos(y*.095-x*.07)+rng.normal(0,.025,(256,256));v=np.clip(v,0,1)
a=np.stack([110+65*v,18+30*v,15+20*v],axis=-1).astype('uint8');Image.fromarray(a).save(R/'lacquer-color.png')
r=(255*(.23+.17*v)).astype('uint8');Image.fromarray(r).save(R/'lacquer-roughness.png')
dy,dx=np.gradient(v);n=np.stack([128-dx*35,128-dy*35,np.full_like(v,255)],-1).clip(0,255).astype('uint8');Image.fromarray(n).save(R/'lacquer-normal.png')
print('MAPS PASS')
