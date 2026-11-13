from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parent; (R/'maps').mkdir(exist_ok=True)
im=Image.new('RGB',(768,512),(229,220,196));d=ImageDraw.Draw(im)
# Original circular eye/flower repeat, not a copied workshop pattern.
for y in range(-32,560,96):
 for x in range(-32,820,96):
  d.ellipse((x-28,y-28,x+28,y+28),fill=(24,59,128))
  d.ellipse((x-20,y-20,x+20,y+20),fill=(229,220,196))
  for k in range(8):
   a=k*np.pi/4;cx=x+14*np.cos(a);cy=y+14*np.sin(a);d.ellipse((cx-3,cy-3,cx+3,cy+3),fill=(24,59,128))
  d.ellipse((x-7,y-7,x+7,y+7),fill=(46,78,56))
  d.ellipse((x+43,y+43,x+49,y+49),fill=(24,59,128))
a=np.array(im).astype(float);rng=np.random.default_rng(713);a+=rng.normal(0,.65,a.shape[:2])[...,None];Image.fromarray(np.clip(a,0,255).astype('uint8')).save(R/'maps/ceramic-color.png')
r=np.clip(68+rng.normal(0,3,(256,256)),50,85).astype('uint8');Image.fromarray(r).convert('RGB').save(R/'maps/ceramic-roughness.png')
print('MAPS PASS')
