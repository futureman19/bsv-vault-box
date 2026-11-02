from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);y,x=np.mgrid[0:256,0:256]/256
v=1-.17*(.5+.5*np.sin((y*90+.2*np.sin(x*9))*6.283))**10+rng.normal(0,.012,x.shape)
for name,c in [('timber-color',[89,60,43]),('plaster-color',[205,185,144]),('stone-color',[118,128,121])]:
 q=v if name.startswith('timber') else 1+rng.normal(0,.035,x.shape)+.025*np.sin(x*22+y*14)
 Image.fromarray(np.uint8(np.clip(q[:,:,None]*np.array(c),0,255))).save(R/(name+'.png'),optimize=True)
Image.fromarray(np.uint8(np.clip(150+(1-v)*100,0,255))).save(R/'timber-roughness.png',optimize=True)
print('MAPS PASS: four procedural 256px maps')
