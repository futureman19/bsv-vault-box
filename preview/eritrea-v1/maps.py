from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(541);n=512
a=rng.random((n,n));coarse=np.asarray(Image.fromarray(np.uint8(rng.random((64,64))*255)).resize((n,n),Image.Resampling.BICUBIC))/255
pores=np.where(a<.035,-rng.uniform(25,65,(n,n)),0)
v=(coarse-.5)*24+(a-.5)*12+pores
color=np.stack([225+v,208+v,172+v],axis=-1).clip(0,255).astype('uint8')
Image.fromarray(color).save(R/'limestone-color.png',optimize=True)
Image.fromarray(np.uint8((207+v*.4).clip(0,255))).save(R/'limestone-roughness.png',optimize=True)
y,x=np.mgrid[0:n,0:n];wave=np.sin(x/37+y/63)*3+np.cos(y/24-x/71)*2
sea=np.stack([19+wave,100+wave*2,112+wave*2],axis=-1).clip(0,255).astype('uint8');Image.fromarray(sea).save(R/'sea-color.png',optimize=True)
print('MAPS_PASS: three generated 512px maps')
