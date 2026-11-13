from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(706);y,x=np.mgrid[0:512,0:512]/512
cloud=np.sin(x*19+np.sin(y*11)*2)+.55*np.sin(y*27+x*9)+.28*np.cos(x*61-y*49)
vein=np.exp(-((np.sin(x*11+y*9+np.sin(y*23)*.32))/.055)**2)
pore=(rng.random(x.shape)>.978)*rng.uniform(10,32,x.shape)
v=cloud*7-vein*12-pore+rng.normal(0,1.8,x.shape)
color=np.stack([188+v,179+v,148+v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'limestone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(184+cloud*14+vein*22+pore,0,255))).save(R/'limestone-roughness.png',optimize=True)
rock=112+rng.normal(0,16,(256,256))
Image.fromarray(np.uint8(np.clip(np.stack([rock*.83,rock*.94,rock],-1),0,255))).save(R/'shale-color.png',optimize=True)
print('PASS procedural maps: limestone color/roughness 512px; shale 256px')
