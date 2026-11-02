"""Original deterministic procedural sandstone maps, not scans."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(179);y,x=np.mgrid[0:512,0:512]/512
# Broad weathering fields, subordinate wind streaks and grain; no copied imagery.
f=.38*np.sin(x*19+np.sin(y*8))+.22*np.sin(y*33+x*5)+.13*np.sin(x*67+y*23)+rng.normal(0,.06,x.shape)
a=np.clip(np.array([183,125,67])[None,None,:]+f[:,:,None]*np.array([40,35,24]),0,255).astype('uint8')
Image.fromarray(a).save(R/'sandstone-color.png',optimize=True)
r=np.clip(198+f*22,160,230).astype('uint8');Image.fromarray(r).save(R/'sandstone-roughness.png',optimize=True)
s=np.clip(np.array([93,65,39])[None,None,:]+f[:,:,None]*np.array([25,22,17]),0,255).astype('uint8');Image.fromarray(s).save(R/'dark-stone.png',optimize=True)
print('MAPS PASS: 3 original 512x512 maps')
