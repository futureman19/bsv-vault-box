from PIL import Image
from pathlib import Path
import random
R=Path(__file__).resolve().parent/'textures';R.mkdir(exist_ok=True)
r=random.Random(523);size=128
h=[[r.random() for x in range(size)] for y in range(size)]
c=Image.new('RGB',(size,size));n=Image.new('RGB',(size,size));rough=Image.new('L',(size,size))
for y in range(size):
 for x in range(size):
  v=int(40+13*h[y][x]);c.putpixel((x,y),(v,v+2,v+3));rough.putpixel((x,y),int(183+35*h[y][x]));dx=h[y][(x+1)%size]-h[y][x];dy=h[(y+1)%size][x]-h[y][x];n.putpixel((x,y),(int(128+dx*30),int(128+dy*30),252))
c.save(R/'stone-color.jpg',quality=80);n.save(R/'stone-normal.png',optimize=True);rough.save(R/'stone-rough.jpg',quality=80)
