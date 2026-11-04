from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(314);y,x=np.mgrid[0:512,0:512]/512
field=x+.33*y+.04*np.sin(y*15)+.018*np.sin(x*24+y*32)+.007*np.sin(y*105+x*41)
vein=np.exp(-(np.sin(field*23)/.065)**2)
minor=np.exp(-(np.sin((field+.018*np.sin(y*40))*49)/.035)**2)*.24
noise=rng.normal(0,1.1,x.shape);value=vein*81+minor*35
rgb=np.stack([218-value+noise,222-value+noise,218-value+noise],-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'marble-color.png')
rough=np.clip(112+vein*39+noise*2,0,255).astype('uint8');Image.fromarray(rough).save(R/'marble-roughness.png')
gy,gx=np.gradient(value/255);n=np.stack([-gx*.32,-gy*.32,np.ones_like(x)],-1);n/=np.linalg.norm(n,axis=-1)[...,None]
Image.fromarray(np.uint8(np.clip((n*.5+.5)*255,0,255))).save(R/'marble-normal.png')
print('MAPS PASS: three generated 512px marble maps')
