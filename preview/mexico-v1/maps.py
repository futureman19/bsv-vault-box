"""Original floral repeat; no traditional workshop pattern or external pixels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,math
R=Path(__file__).resolve().parent;D=R/'maps';D.mkdir(exist_ok=True)
N=1024
im=Image.new('RGB',(N,N),'#e6ddc4');d=ImageDraw.Draw(im)
blue='#173b75';ochre='#bb893b'
d.rounded_rectangle((25,25,999,999),radius=70,outline=blue,width=19)
d.rounded_rectangle((51,51,973,973),radius=60,outline=ochre,width=6)
# Eight curved almond petals, independent original geometry.
for j in range(8):
 a=j*math.tau/8
 pts=[]
 for k in range(41):
  t=k/40;r=85+295*t;w=72*math.sin(math.pi*t)
  pts.append((512+math.cos(a)*r-math.sin(a)*w,512+math.sin(a)*r+math.cos(a)*w))
 for k in range(40,-1,-1):
  t=k/40;r=85+295*t;w=72*math.sin(math.pi*t)
  pts.append((512+math.cos(a)*r+math.sin(a)*w,512+math.sin(a)*r-math.cos(a)*w))
 d.polygon(pts,fill=blue)
 for r in [165,230,295]:
  x=512+math.cos(a)*r;y=512+math.sin(a)*r;d.ellipse((x-8,y-8,x+8,y+8),fill='#e6ddc4')
d.ellipse((461,461,563,563),fill=ochre,outline=blue,width=10)
for x in [130,894]:
 for y in [130,894]:d.ellipse((x-31,y-31,x+31,y+31),fill=blue)
im=im.resize((512,512),Image.Resampling.LANCZOS);im.save(D/'ceramic-color.png')
rng=np.random.default_rng(1462);a=np.asarray(im);noise=rng.normal(0,2,(512,512));rough=np.clip(100+noise+18*(a[:,:,2]<140),0,255).astype('uint8');Image.fromarray(rough).convert('RGB').save(D/'ceramic-roughness.png')
y,x=np.mgrid[:256,:256];n=rng.normal(0,1,(256,256));v=5*np.sin(x*.12)*np.sin(y*.08)+n*3
rgb=np.stack([163+v,85+v*.8,52+v*.6],axis=2).clip(0,255).astype('uint8');Image.fromarray(rgb).save(D/'terracotta-color.png')
print('MAPS PASS: 512 ceramic color/roughness, 256 terracotta; original procedural pixels')
