from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter,ImageDraw
R=Path(__file__).resolve().parent;D=R/'maps';D.mkdir(exist_ok=True)
rng=np.random.default_rng(139)
noise=rng.integers(0,256,(64,64),dtype=np.uint8)
low=np.array(Image.fromarray(noise).resize((512,512),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(3)),dtype=float)/255-.5
fine=rng.normal(0,2,(512,512))
base=np.stack([168+low*35+fine,93+low*26+fine,57+low*18+fine],axis=-1)
im=Image.fromarray(np.uint8(np.clip(base,0,255)));draw=ImageDraw.Draw(im,'RGB')
for i in range(6200):
 x,y=rng.integers(0,512,2);dx=int(rng.integers(-7,8));dy=int(rng.integers(2,12));v=int(rng.integers(-12,13));draw.line((int(x),int(y),int(x+dx),int(y+dy)),fill=(168+v,93+v,57+v),width=1)
im.save(D/'barkcloth-color.png')
Image.fromarray(np.uint8(np.array(im)*.70)).save(D/'barkcloth-edge.png')
rough=np.uint8(np.clip(193+low*35+fine,0,255));Image.fromarray(rough).convert('RGB').save(D/'barkcloth-roughness.png')
g=rng.integers(48,94,(128,128),dtype=np.uint8);Image.fromarray(g).convert('RGB').save(D/'granite.png')
print('MAPS_PASS')
