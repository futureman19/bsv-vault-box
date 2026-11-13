from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(174);y,x=np.mgrid[0:512,0:512]/512
# Warped Voronoi clasts: independently generated, no source-image pixels.
xw=x+.008*np.sin(y*31+x*12);yw=y+.007*np.sin(x*26-y*9)
pts=rng.uniform(-.15,1.15,(95,2));d=np.stack([(xw-a)**2+(yw-b)**2 for a,b in pts]);order=np.argsort(d,axis=0);near=np.take_along_axis(d,order[:2],axis=0)
bound=np.sqrt(near[1])-np.sqrt(near[0]);cement=np.clip((.007-bound)/.005,0,1)
v=rng.uniform(.78,1.17,len(pts))[order[0]]+.04*np.sin(x*73+y*39)+rng.normal(0,.012,x.shape)
base=np.stack([151*v,61*v,59*v],-1);ivory=np.array([217,199,173]);rgb=base*(1-cement[...,None])+ivory*cement[...,None]
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'adnet-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(rgb*.70,0,255))).resize((256,256)).save(R/'adnet-edge.png',optimize=True)
Image.fromarray(np.uint8(82+cement*32+np.clip(v-.7,0,1)*24)).save(R/'adnet-roughness.png',optimize=True)
speck=np.clip(100+rng.normal(0,14,(256,256)),45,155)
Image.fromarray(np.uint8(np.stack([speck*.9,speck,speck*1.02],-1))).save(R/'granite.png',optimize=True)
print('MAPS PASS', 'cement fraction',float((cement>.5).mean()))
