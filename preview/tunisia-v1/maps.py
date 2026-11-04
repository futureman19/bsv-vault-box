from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1406);n=512
y,x=np.mgrid[:n,:n];noise=rng.normal(0,1.5,(n,n))+2*np.sin(x/43)*np.cos(y/36)
a=np.clip(np.array([205,181,143])[None,None,:]+noise[:,:,None],0,255).astype('uint8')
im=Image.fromarray(a);d=ImageDraw.Draw(im)
for yy in [80,420]:
 d.line([(0,yy-18),(512,yy-18)],fill=(145,55,34),width=5)
 d.line([(0,yy+18),(512,yy+18)],fill=(145,55,34),width=5)
 for xx in range(-16,528,32):
  d.line([(xx,yy-11),(xx+16,yy+11),(xx+32,yy-11)],fill=(42,34,29),width=4)
im.save(R/'clay-color.png')
plain=np.clip(np.array([183,115,72])[None,None,:]+noise[:,:,None],0,255).astype('uint8');Image.fromarray(plain).save(R/'clay-plain.png')
Image.fromarray(np.clip(170+noise*3,0,255).astype('uint8')).convert('RGB').save(R/'clay-roughness.png')
print('MAPS PASS')
