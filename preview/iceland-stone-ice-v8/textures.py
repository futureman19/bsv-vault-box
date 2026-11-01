from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parent/'textures';R.mkdir(exist_ok=True)
rng=np.random.default_rng(808);n=512
fine=rng.normal(0,1,(n,n));medium=np.array(Image.fromarray(np.uint8(rng.uniform(0,255,(128,128)))).resize((n,n),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(1)),dtype=float)/255-.5
# Fine mineral grain with shallow pore relief, no broad cloud pattern.
h=.27*fine+.55*medium;pores=rng.random((n,n))<.045;h[pores]-=1.5
h=np.array(Image.fromarray(np.uint8(np.clip(128+28*h,0,255))).filter(ImageFilter.GaussianBlur(.45)),dtype=float)/255
v=np.clip(64+11*fine+19*medium-17*pores,28,100)
a=np.stack([v*.93,v*.98,v*1.025],axis=2).clip(0,255).astype('uint8');Image.fromarray(a).save(R/'stone-color.jpg',quality=88,optimize=True)
y,x=np.gradient(h);norm=np.stack([-x*2.0,-y*2.0,np.ones_like(h)],axis=2);norm/=np.linalg.norm(norm,axis=2)[:,:,None]
Image.fromarray(np.uint8((norm*.5+.5)*255)).save(R/'stone-normal.jpg',quality=90,optimize=True)
Image.fromarray(np.uint8(np.clip(204+fine*9+medium*18,170,235))).save(R/'stone-rough.jpg',quality=83,optimize=True)
print({p.name:p.stat().st_size for p in R.iterdir()})
