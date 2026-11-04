from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,math
R=Path(__file__).resolve().parent;D=R/'maps';D.mkdir(exist_ok=True)
N=512;im=Image.new('RGB',(N,N),(231,229,214));d=ImageDraw.Draw(im)
# Invented cobalt floral cartouches, independently drawn; no copied museum pixels.
for cy in [128,384]:
 for cx in [128,384]:
  for radius,w in [(98,3),(91,1)]:d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=(28,65,117),width=w)
  for k in range(8):
   a=k*math.tau/8;pts=[]
   for j in range(41):
    t=j*math.tau/40;r=24+22*math.cos(t);s=10*math.sin(t)
    pts.append((cx+r*math.cos(a)-s*math.sin(a),cy+r*math.sin(a)+s*math.cos(a)))
   d.polygon(pts,fill=(31+3*k,75+2*k,129+2*k))
  d.ellipse((cx-10,cy-10,cx+10,cy+10),fill=(20,52,105))
  for k in range(16):
   a=k*math.tau/16;x=cx+76*math.cos(a);y=cy+76*math.sin(a);d.ellipse((x-3,y-3,x+3,y+3),fill=(26,64,116))
for y in [3,9,250,256,262,503,509]:d.line((0,y,511,y),fill=(29,70,125),width=2)
rng=np.random.default_rng(123);a=np.array(im).astype(float);a+=rng.normal(0,.7,(N,N,1));Image.fromarray(np.uint8(np.clip(a,0,255))).save(D/'delft-color.png',optimize=True)
r=np.uint8(np.clip(81+rng.normal(0,3,(N,N)),65,99));Image.fromarray(r).convert('RGB').save(D/'delft-roughness.png',optimize=True)
print('MAPS PASS')
