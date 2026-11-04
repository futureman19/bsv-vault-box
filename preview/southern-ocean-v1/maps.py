from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:384,0:512];x=x/512;y=y/384
warp=y+.08*np.sin(x*10+y*6)+.025*np.sin(x*23-y*12)
w=(.5+.5*np.sin(warp*39+x*3))**12
fine=np.random.default_rng(521).normal(0,1,(384,512))
a=np.stack([18+18*w+fine,56+43*w+fine,73+49*w+fine],axis=-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'ocean-color.png')
r=np.uint8(np.clip(110+32*w+fine,0,255));Image.fromarray(r).convert('RGB').save(R/'ocean-roughness.png')
dy,dx=np.gradient(w);n=np.stack([128-45*dx,128-45*dy,np.full_like(w,255)],axis=-1);Image.fromarray(np.uint8(np.clip(n,0,255))).save(R/'ocean-normal.png')
print('MAPS PASS')
