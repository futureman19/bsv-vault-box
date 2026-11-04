"""Original procedural decorative frieze. No copied artist imagery."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,math
R=Path(__file__).resolve().parent;M=R/'maps';M.mkdir(exist_ok=True)
rng=np.random.default_rng(893);w,h=1024,512
y,x=np.mgrid[:h,:w];grain=np.sin(y*.9+np.sin(x*.024)*2)*1.7+rng.normal(0,.65,(h,w))
a=np.clip(np.array([23,35,28])[None,None,:]+grain[:,:,None],0,255).astype('uint8')
wood=Image.fromarray(a);wood.save(M/'wood-color.png');im=wood.copy();d=ImageDraw.Draw(im)
# Compositional stems and brush-like tapering leaves are new artwork.
for side in [-1,1]:
 pts=[(512+side*t,330-int(65*math.sin(t/420*math.pi))) for t in range(0,450,5)];d.line(pts,fill=(72,116,45),width=8)
 for t in [110,205,300,380]:
  px=512+side*t;py=330-int(65*math.sin(t/420*math.pi))
  for s in [-1,1]:
   d.polygon([(px,py),(px+side*20,py+s*70),(px+side*65,py+s*100),(px+side*54,py+s*35)],fill=(73+t//9,132,52))
   d.line([(px,py),(px+side*60,py+s*90)],fill=(151,164,70),width=2)
for cx,cy,r in [(160,220,62),(345,170,72),(680,175,72),(865,225,60)]:
 d.line([(cx,cy),(cx,300)],fill=(90,138,52),width=5)
 for j in range(13):
  a=j*math.tau/13;ux,uy=math.cos(a),math.sin(a);vx,vy=-uy,ux
  pts=[(cx+ux*r*.18,cy+uy*r*.18),(cx+ux*r*.7+vx*r*.18,cy+uy*r*.7+vy*r*.18),(cx+ux*r,cy+uy*r),(cx+ux*r*.7-vx*r*.18,cy+uy*r*.7-vy*r*.18)]
  d.polygon(pts,fill=(221,49+(j%3)*10,33))
 d.ellipse((cx-r*.25,cy-r*.25,cx+r*.25,cy+r*.25),fill=(231,171,54))
 for j in range(8):
  a=j*math.tau/8;px=cx+math.cos(a)*r*.13;py=cy+math.sin(a)*r*.13;d.ellipse((px-2,py-2,px+2,py+2),fill=(86,65,21))
# Restrained double-rule border, leaving enough lacquer visible.
for yy in [40,46,465,471]:d.line([(30,yy),(994,yy)],fill=(168,126,49),width=2)
im.save(M/'floral-color.png')
rough=np.clip(96+grain*3,0,255).astype('uint8');Image.fromarray(rough).save(M/'lacquer-roughness.png')
print('MAPS PASS',len(list(M.glob('*.png'))))
