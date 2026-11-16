"""Original deterministic painted flag-inspired maps; no image generation/download."""
from pathlib import Path
from PIL import Image,ImageDraw
import math,numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
N=1024;RED=(183,23,43);WHITE=(239,235,218);NAVY=(12,30,69)
def star(d,x,y,r):
 pts=[(x+math.sin(i*math.pi/5)*r*(1 if i%2==0 else .42),y-math.cos(i*math.pi/5)*r*(1 if i%2==0 else .42)) for i in range(10)];d.polygon(pts,fill=WHITE)
for name,rows,cols in [('flag-wall.png',3,4),('flag-lid.png',5,6)]:
 im=Image.new('RGB',(N,N));d=ImageDraw.Draw(im)
 for i in range(7):d.rectangle((0,int(i*N/7),N,int((i+1)*N/7)),fill=RED if i%2==0 else WHITE)
 cw=int(.46*N);ch=int(N*4/7);d.rectangle((0,0,cw,ch),fill=NAVY)
 for row in range(rows):
  count=cols if row%2==0 else cols-1
  for col in range(count):star(d,(col+1)*(cw/(count+1)),(row+.65)*ch/rows,min(cw/(cols+1),ch/rows)*.36)
 im.save(R/name,optimize=True)
y,x=np.mgrid[:256,:256];a=(68+3*np.sin(x*.17)*np.cos(y*.23)).astype('uint8');Image.fromarray(a).save(R/'lacquer-roughness.png')
print('3 maps generated')
