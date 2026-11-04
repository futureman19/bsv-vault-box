from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
r=random.Random(754)
im=Image.new('RGB',(512,512));pix=im.load()
for y in range(512):
 for x in range(512):
  n=r.randrange(-8,9);pix[x,y]=(18+n,48+n,67+n)
d=ImageDraw.Draw(im)
for i in range(22):
 x,y=r.randrange(512),r.randrange(512);points=[(x,y)]
 for j in range(r.randrange(4,10)):
  x+=r.randrange(-45,46);y+=r.randrange(15,50);points.append((x,y))
 d.line(points,fill=(125,204,220),width=1)
 if i%2==0:
  x,y=points[2];d.line([(x,y),(x+35,y+9),(x+58,y-17)],fill=(80,150,175),width=1)
im.save(R/'ice-color.png')
rough=Image.new('L',(512,512));rough.putdata([r.randrange(65,115) for _ in range(512*512)]);rough=rough.filter(ImageFilter.GaussianBlur(.7));rough.save(R/'ice-roughness.png')
mineral=Image.new('RGB',(256,256));mineral.putdata([(v,v+8,v+15) for v in [r.randrange(15,65) for _ in range(256*256)]]);mineral.save(R/'mineral.png')
print('MAPS PASS')
