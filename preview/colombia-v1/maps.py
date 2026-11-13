from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1121);y,x=np.mgrid[0:512,0:512]/512
fine=(.5+.5*np.sin((x*150+.2*np.sin(y*7))*6.283))**10
canes=(.5+.5*np.sin(x*18*6.283))**24
nodes=np.exp(-((np.sin((y*3+.07*np.sin(x*18*6.283))*np.pi))/.10)**2)
v=1-.12*fine-.22*canes-.27*nodes+.045*np.sin(x*27)+rng.normal(0,.008,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([181*v,140*v,70*v],-1),0,255))).save(R/'bamboo-color.png')
Image.fromarray(np.uint8(np.clip(154+fine*22+nodes*39,0,255))).save(R/'bamboo-roughness.png')
s=np.clip(rng.normal(95,17,(256,256)),30,170)
Image.fromarray(np.uint8(np.stack([s,s*.98,s*.88],-1))).save(R/'stone.png')
print('MAPS PASS: 512px bamboo color/roughness, 256px stone')
