from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521)
n=512
noise=rng.normal(0,1.7,(n,n,1))
for name,col in [('clay',(183,95,61)),('ivory',(238,224,191))]:
 a=np.clip(np.array(col)[None,None,:]+noise,0,255).astype('uint8');Image.fromarray(a).save(R/(name+'-color.png'))
Image.fromarray(np.clip(105+noise[:,:,0]*2,0,255).astype('uint8')).save(R/'glaze-roughness.png')
# Original repeat, not a traced cultural motif. Ivory field with cobalt leaves.
im=Image.new('RGB',(512,512),(238,224,191));d=ImageDraw.Draw(im)
for cy in range(64,512,128):
 for cx in range(64,512,128):
  for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]:
   px,py=-dy,dx
   d.polygon([(cx+dx*8,cy+dy*8),(cx+dx*30+px*13,cy+dy*30+py*13),(cx+dx*53,cy+dy*53),(cx+dx*30-px*13,cy+dy*30-py*13)],fill=(33,76,141))
  d.ellipse((cx-8,cy-8,cx+8,cy+8),fill=(197,145,54))
im.save(R/'ceramic-pattern.png')
print('MAPS PASS')
