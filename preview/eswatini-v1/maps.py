from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(748);y,x=np.mgrid[0:256,0:512]
# Alternating over-under bands with subordinate fiber strands, no image inputs.
w=(x//12+y//10)%2
strand=.5+.5*np.sin((x*(1-w)+y*w)*2.5)
edge=np.minimum(x%12,11-x%12)*(1-w)+np.minimum(y%10,9-y%10)*w
v=.80+.18*np.minimum(edge/2,1)-.08*strand+rng.normal(0,.018,x.shape)
c=np.stack([204*v,163*v,96*v],-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'grass-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(180+strand*35,0,255))).save(R/'grass-roughness.png',optimize=True)
binding_v=.82+(v-.82)*2.0
b=np.stack([87*binding_v,53*binding_v,32*binding_v],-1)
Image.fromarray(np.uint8(np.clip(b,0,255))).resize((256,128)).save(R/'binding.png',optimize=True)
print('MAPS PASS: original generated weave, roughness, binding')
