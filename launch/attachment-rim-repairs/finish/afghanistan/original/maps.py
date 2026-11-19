from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(774);y,x=np.mgrid[0:512,0:512]/512
f=np.sin(x*18+y*7+2*np.sin(y*12))+ .42*np.sin(y*28-x*9)+.2*np.sin(x*57+y*31)
vein=np.exp(-((f-.25)/.047)**2)*.75
v=.82+.13*np.sin(x*11+y*14)+.08*np.sin(x*39-y*19)+rng.normal(0,.017,x.shape)
col=np.stack([33*v,70*v,157*v],-1);col=col*(1-vein[...,None])+np.array([200,192,158])*vein[...,None]
flecks=rng.random(x.shape)>.994;col[flecks]=[174,140,61]
Image.fromarray(np.uint8(np.clip(col,0,255))).save(R/'lapis-color.png')
rough=np.clip(100+vein*65+rng.normal(0,3,x.shape),0,255)
Image.fromarray(np.uint8(rough)).save(R/'lapis-roughness.png')
gy,gx=np.gradient(f*.004+vein*.02);normal=np.stack([-gx*8,-gy*8,np.ones_like(x)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8(np.clip((normal*.5+.5)*255,0,255))).save(R/'lapis-normal.png')
m=158+18*np.sin(x*14+y*19)+10*np.sin(x*47-y*27)+rng.normal(0,4,x.shape)
Image.fromarray(np.uint8(np.stack([m,m*.95,m*.84],-1))).resize((256,256)).save(R/'marble.png')
print('PASS procedural lapis color/roughness/normal and marble maps')
