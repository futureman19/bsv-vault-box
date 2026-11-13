from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(764);n=rng.normal(0,1,(256,256));p=rng.random((256,256))<.035
v=n*4-p*25
color=np.stack([210+v,194+v,155+v],axis=2)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'stone-color.png')
Image.fromarray(np.uint8(np.clip(190+n*10+p*22,0,255))).save(R/'stone-roughness.png')
y,x=np.gradient(v*.0015);a=np.stack([-x,-y,np.ones_like(x)],axis=2);a/=np.linalg.norm(a,axis=2)[:,:,None]
Image.fromarray(np.uint8(np.clip((a*.5+.5)*255,0,255))).save(R/'stone-normal.png')
print('MAPS PASS')
