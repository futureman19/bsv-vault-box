from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(271);y,x=np.mgrid[0:512,0:512]/512
phase=y*34+.19*np.sin(x*21+y*8)+.09*np.sin(x*53)
vein=np.exp(-((np.sin(phase*6.283))/.20)**2)
v=1-.13*vein+.045*np.sin(y*40+x*9)+rng.normal(0,.029,x.shape)
a=np.stack([171*v,156*v,129*v],-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'sandstone-color.png')
Image.fromarray(np.uint8(np.clip(a*.8,0,255))).resize((256,256)).save(R/'sandstone-detail.png')
Image.fromarray(np.uint8(np.clip(174+vein*37+rng.normal(0,4,x.shape),0,255))).save(R/'sandstone-roughness.png')
g=np.clip(rng.normal(100,25,(256,256)),30,180);Image.fromarray(np.uint8(np.stack([g*1.03,g,g*.97],-1))).save(R/'granite.png')
print('MAPS PASS')
