from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np, math
R=Path(__file__).resolve().parent;D=R/'maps';D.mkdir(exist_ok=True)
im=Image.new('RGB',(512,512),(25,143,152));d=ImageDraw.Draw(im)
for x in range(-128,641,256):
 for y in range(-128,641,256):
  pts=[(x+(102 if k%2==0 else 64)*math.cos(k*math.pi/8),y+(102 if k%2==0 else 64)*math.sin(k*math.pi/8)) for k in range(16)]
  d.polygon(pts,fill=(21,43,88));d.line(pts+[pts[0]],fill=(233,221,181),width=5)
  pts=[(x+(63 if k%2==0 else 39)*math.cos(k*math.pi/8),y+(63 if k%2==0 else 39)*math.sin(k*math.pi/8)) for k in range(16)]
  d.polygon(pts,fill=(233,221,181));d.ellipse((x-18,y-18,x+18,y+18),fill=(25,143,152))
rng=np.random.default_rng(115);arr=np.asarray(im).astype(float);noise=rng.normal(0,1.2,(512,512,1));Image.fromarray(np.uint8(np.clip(arr+noise,0,255))).save(D/'ceramic-color.png')
rough=np.uint8(np.clip(85+rng.normal(0,5,(512,512)),65,110));Image.fromarray(rough).save(D/'ceramic-roughness.png')
print('MAPS PASS 512x512 color and roughness')
