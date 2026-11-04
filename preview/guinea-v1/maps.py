from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(155);n=512
# Multi-scale isotropic mineral noise, no copied photographs or wood bands.
field=np.zeros((n,n))
for size,weight in [(8,.45),(32,.3),(128,.15),(512,.1)]:
 a=Image.fromarray(np.uint8(rng.random((size,size))*255)).resize((n,n),Image.Resampling.BICUBIC)
 field+=np.asarray(a)/255*weight
field=np.clip((field-.5)*2+.5,0,1)
lo=np.array([100,48,30]);hi=np.array([187,119,77]);rgb=np.uint8(lo+field[...,None]*(hi-lo))
Image.fromarray(rgb).save(R/'earth-color.png')
Image.fromarray(np.uint8(rgb*.70)).save(R/'earth-dark.png')
Image.fromarray(np.uint8(165+field*65)).save(R/'earth-roughness.png')
rock=np.uint8(55+field*115);Image.fromarray(np.stack([rock,np.uint8(rock*.9),np.uint8(rock*.73)],axis=-1)).save(R/'granite.png')
print('MAPS PASS 4 generated 512x512 textures')
