"""Original deterministic painted flag-inspired maps; no image generation/download."""
from pathlib import Path
from PIL import Image,ImageDraw
import math,numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
N=1024;RED=(183,23,43);WHITE=(239,235,218);NAVY=(12,30,69)
def star(d,x,y,r):
 pts=[(x+math.sin(i*math.pi/5)*r*(1 if i%2==0 else .42),y-math.cos(i*math.pi/5)*r*(1 if i%2==0 else .42)) for i in range(10)];d.polygon(pts,fill=WHITE)
# Single rear-right-seamed perimeter interval; no per-face repeats.
for name,w,h,x0,x1,rows,cols in [('flag-wall.png',2048,256,2.01/12.4,7.91/12.4,3,15),('flag-lid.png',768,512,0,1.71/3.72,6,5)]:
 im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im)
 for i in range(7):d.rectangle((0,int(i*h/7),w,int((i+1)*h/7)),fill=RED if i%2==0 else WHITE)
 bottom=int(h*3/7) if 'wall' in name else h
 d.rectangle((int(x0*w),0,int(x1*w),bottom),fill=NAVY)
 for row in range(rows):
  count=cols if row%2==0 else cols-1
  for col in range(count):
   xx=(x0+(col+1)*(x1-x0)/(count+1))*w;yy=(row+.5)*bottom/rows
   rx=w/(12.4 if 'wall' in name else 3.72)*.065;ry=h/(1.46 if 'wall' in name else 2.38)*.065
   d.polygon([(xx+math.sin(i*math.pi/5)*rx*(1 if i%2==0 else .42),yy-math.cos(i*math.pi/5)*ry*(1 if i%2==0 else .42)) for i in range(10)],fill=WHITE)
 im.save(R/name,optimize=True)
y,x=np.mgrid[:256,:256];a=(68+3*np.sin(x*.17)*np.cos(y*.23)).astype('uint8');Image.fromarray(a).save(R/'lacquer-roughness.png')
print('3 maps generated')
