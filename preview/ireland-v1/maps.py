from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(731);y,x=np.mgrid[0:512,0:512]/512
warp=y*5+x*1.2+.26*np.sin(x*11+y*5)+.15*np.sin(x*22-y*9)
a=np.sin(warp*6.283);fine=np.sin(warp*43+.8*np.sin(x*29))
pale=np.clip((a-.45)*2.1,0,1);dark=np.clip((-fine-.5)*1.4,0,1)
base=np.stack([55+112*pale,88+94*pale,53+90*pale],-1)
base*=1-.24*dark[...,None];base+=rng.normal(0,1.8,base.shape)
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'marble-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(base*.6,0,255))).resize((256,256)).save(R/'marble-dark.png',optimize=True)
Image.fromarray(np.uint8(85+32*pale+23*dark)).save(R/'marble-roughness.png',optimize=True)
y,x=np.mgrid[0:256,0:256]/256
v=170+10*np.sin(x*13+y*9)+7*np.sin(y*36)+rng.normal(0,4,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([v*1.03,v*1.025,v],-1),0,255))).save(R/'limestone.png',optimize=True)
print('PASS procedural maps')
