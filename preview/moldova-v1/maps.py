from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];rng=np.random.default_rng(521)
# Larger staggered thread bundles remain legible at normal object size.
warp=((x//8+y//8)%2==0)
thread=np.where(warp, 18*np.cos((x%8-3.5)*.39), 18*np.cos((y%8-3.5)*.39))-7+rng.normal(0,1.5,x.shape)
c=np.zeros((512,512,3))+[43,35,33]
border=(y<62)|(y>449)
diamond=(np.abs((x%64)-32)+np.abs((y%64)-32)<22)
c[border&diamond]=[196,164,109];c[border&~diamond]=[99,36,49]
# Interior small stepped diamonds woven into dark ground.
f=(np.abs((x%128)-64)+np.abs((y%128)-64)<16)&~border
c[f]=[116,56,65]
c=np.clip(c+thread[:,:,None],0,255).astype('uint8');Image.fromarray(c).save(R/'weave-color.png')
r=np.clip(190+thread*2,0,255).astype('uint8');Image.fromarray(r).save(R/'weave-roughness.png')
dy,dx=np.gradient(thread)
n=np.zeros((512,512,3),dtype='uint8');n[:]=[128,128,245];n[:,:,0]=np.clip(128-dx*5,0,255);n[:,:,1]=np.clip(128-dy*5,0,255);Image.fromarray(n).save(R/'weave-normal.png')
grain=7*np.sin(y*.45+2*np.sin(x*.023))+4*np.sin(y*1.6)+rng.normal(0,1.5,x.shape)
w=np.clip(np.array([95,54,32])+grain[:,:,None],0,255).astype('uint8');Image.fromarray(w).save(R/'walnut-color.png')
print('MAPS PASS')
