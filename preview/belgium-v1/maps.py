from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(514)
v=rng.normal(0,2,(512,512));rgb=np.stack([59+v,72+v,83+v],-1)
im=Image.fromarray(np.uint8(np.clip(rgb,0,255)));d=ImageDraw.Draw(im)
for i in range(520):
 x,y=rng.integers(0,512,2);r=int(rng.integers(1,5));shade=int(rng.integers(115,190));d.ellipse((x-r,y-r,x+r,y+r),outline=(shade,shade+3,shade+4),width=1)
for i in range(20):
 x,y=rng.integers(0,512,2);d.line([(int(x),int(y)),(int(x+7),int(y-2)),(int(x+13),int(y-1))],fill=(99,113,120),width=1)
im.save(R/'stone-color.png',optimize=True)
Image.fromarray(np.uint8(np.array(im)*.70)).save(R/'lid-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(155+v*5,100,200))).save(R/'stone-roughness.png',optimize=True)
print('MAPS PASS')
