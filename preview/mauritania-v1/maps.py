"""Original deterministic mineral maps; no reference-image pixels."""
from pathlib import Path
import math,random
from PIL import Image
R=Path(__file__).resolve().parent;(R/'maps').mkdir(exist_ok=True)
rng=random.Random(2301)
color=Image.new('RGB',(512,256));rough=Image.new('L',(512,256));slate=Image.new('RGB',(512,256))
clamp=lambda n:max(0,min(255,round(n)))
for y in range(256):
 for x in range(512):
  u=x/512;v=y/256;warp=v+.028*math.sin(u*17)+.009*math.sin(u*43+v*7)
  bands=math.sin(warp*85+1.2*math.sin(warp*21))*.5+.5
  fine=rng.gauss(0,1);vein=math.exp(-((math.sin(warp*113+u*3))/.12)**2)
  color.putpixel((x,y),tuple(map(clamp,(178+24*bands-17*vein+fine*3,130+29*bands-14*vein+fine*3,78+31*bands-9*vein+fine*2))))
  rough.putpixel((x,y),clamp(190+25*bands+fine*6))
  slate.putpixel((x,y),tuple(map(clamp,(78+fine*7+bands*19,88+fine*7+bands*17,89+fine*6+bands*14))))
color.save(R/'maps/ochre-color.png');rough.save(R/'maps/mineral-roughness.png');slate.save(R/'maps/slate-color.png')
print('MAPS PASS: 3 original 512x256 maps')
