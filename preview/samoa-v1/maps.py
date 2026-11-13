"""Original deterministic siapo-inspired ink repeats, not a copied traditional design."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1261);s=512
im=Image.new('RGB',(s,s),(218,195,154));d=ImageDraw.Draw(im)
# Four large leaf/lozenge cells per axis; restrained alternating ink colours.
for j in range(4):
 for i in range(4):
  x=i*128;y=j*128;c=(111,66,42) if (i+j)%2 else (167,89,54)
  d.rectangle((x+5,y+5,x+122,y+122),outline=(48,36,31),width=4)
  d.polygon([(x+64,y+14),(x+112,y+64),(x+64,y+114),(x+16,y+64)],outline=c,width=6)
  for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
   d.polygon([(x+64,y+64),(x+64+dx*35,y+64+dy*13),(x+64+dx*34,y+64+dy*34),(x+64+dx*13,y+64+dy*35)],fill=c)
  d.ellipse((x+58,y+58,x+70,y+70),fill=(48,36,31))
a=np.array(im).astype(float);grain=rng.normal(0,2.4,(s,s))+rng.normal(0,1,(s,1));a=np.clip(a+grain[:,:,None],0,255).astype('uint8');Image.fromarray(a).save(R/'siapo-color.png')
rough=np.clip(210+grain*2,180,236).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'siapo-roughness.png')
noise=rng.normal(0,7,(s,s));broad=np.asarray(Image.fromarray(rng.integers(0,255,(32,32),dtype='uint8')).resize((s,s),Image.Resampling.BICUBIC)).astype(float)/255
v=noise+(broad-.5)*24
lava=np.clip(np.array([52,58,55])+v[:,:,None],0,255).astype('uint8');Image.fromarray(lava).save(R/'lava-color.png')
Image.fromarray(np.clip(216+v,175,245).astype('uint8')).convert('RGB').save(R/'lava-roughness.png')
print('MAPS_PASS 4 procedural 512x512 maps')
