from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(481);n=512;y,x=np.mgrid[0:n,0:n]/n
xx=x+.035*np.sin(y*19)+.012*np.sin(y*53+x*22);yy=y+.03*np.sin(x*23)+.012*np.cos(y*33-x*40)
seeds=rng.random((44,2));ds=np.stack([((xx-a+.5)%1-.5)**2+((yy-b+.5)%1-.5)**2 for a,b in seeds]);d=np.sort(ds,axis=0)
vein=np.exp(-((np.sqrt(d[1])-np.sqrt(d[0]))/.011)**2)
cloud=(np.sin(x*21+y*16)+np.sin(y*37-x*12))*.5
base=np.stack([65+25*cloud,164+21*cloud,192+18*cloud],axis=-1);color=base*(1-vein[...,None]*.83)+np.array([231,244,235])*vein[...,None]*.83
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'larimar-color.png')
rough=np.uint8(np.clip(72+vein*32+cloud*9,0,255));Image.fromarray(rough).save(R/'larimar-roughness.png')
gy,gx=np.gradient(vein*.25+cloud*.04);normal=np.stack([-gx*3,-gy*3,np.ones_like(gx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1)[...,None]
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'larimar-normal.png')
print('MAPS PASS')
