"""Original procedural weaving-inspired maps; no third-party pixels."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;D=R/'maps';D.mkdir(exist_ok=True)
rng=np.random.default_rng(879);n=512;y,x=np.mgrid[:n,:n]
# Subtle crossed threads under a spacious staggered supplementary motif field.
thread=2.3*np.sin(x*np.pi/2)+1.7*np.sin(y*np.pi/2)+rng.normal(0,.6,(n,n))
a=np.clip(np.array([22,77,80])+thread[:,:,None],0,255).astype('uint8')
im=Image.fromarray(a);draw=ImageDraw.Draw(im)
for row,cy in enumerate(range(32,512,64)):
 for cx in range(32+(row%2)*32,544,64):
  # Independent stepped lozenge and four small petal diamonds, not copied traditional motif.
  for yy in range(-12,13,3):
   w=12-abs(yy);draw.rectangle((cx-w,cy+yy,cx+w,cy+yy+1),fill=(230,213,173))
  for dx,dy in [(0,-20),(0,20),(-20,0),(20,0)]:
   draw.polygon([(cx+dx,cy+dy-3),(cx+dx+3,cy+dy),(cx+dx,cy+dy+3),(cx+dx-3,cy+dy)],fill=(193,171,125))
im.save(D/'jamdani-color.png',optimize=True)
Image.fromarray(np.clip(150+thread*2,0,255).astype('uint8')).save(D/'weave-roughness.png')
# Compact small-scale threads: shallow normal response, no fake heavy embossed cloth.
norm=np.stack([128+3*np.cos(x*np.pi/2),128+3*np.cos(y*np.pi/2),np.full_like(x,255)],axis=2).astype('uint8');Image.fromarray(norm).save(D/'weave-normal.png')
land=np.clip(np.array([44,88,50])+rng.normal(0,3,(n,n,1))+6*np.sin(x[:,:,None]/31)*np.cos(y[:,:,None]/23),0,255).astype('uint8');Image.fromarray(land).save(D/'delta-green.png')
print('MAPS PASS: four original 512px maps')
