from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
im=Image.new('RGB',(512,512),(230,223,204));d=ImageDraw.Draw(im)
# Original fourfold botanical tile, painted procedurally at high working resolution.
for cx,cy in [(128,128),(384,128),(128,384),(384,384)]:
 d.ellipse((cx-99,cy-99,cx+99,cy+99),outline=(23,62,131),width=7)
 for a in range(8):
  t=a*np.pi/4; vx,vy=np.cos(t),np.sin(t);px,py=-vy,vx
  pts=[(cx+vx*r+px*w,cy+vy*r+py*w) for r,w in [(18,0),(52,17),(86,0),(52,-17)]]
  d.polygon(pts,fill=(23,62,131) if a%2 else (40,141,153))
 d.ellipse((cx-15,cy-15,cx+15,cy+15),fill=(187,57,49))
im.save(R/'ceramic-color.png',optimize=True)
y,x=np.mgrid[:256,:256];v=110+15*np.sin(x*.12)*np.sin(y*.09)
Image.fromarray(v.astype('uint8')).save(R/'ceramic-roughness.png',optimize=True)
Image.fromarray((v*.7).astype('uint8')).save(R/'cobalt-roughness.png',optimize=True)
print('PASS procedural ceramic maps')
