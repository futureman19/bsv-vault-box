from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);y,x=np.mgrid[0:256,0:256];n=rng.normal(0,1,(256,256))
a=.5+.16*np.sin(x*.031+y*.025)+.1*np.sin(y*.09+np.sin(x*.05))+.035*n
# Invented interrupted resist-like marks, not a documented traditional pattern.
marks=np.exp(-(np.sin(x*.052+.45*np.sin(y*.04))/.13)**2)*np.exp(-(np.sin(y*.065+.3*np.sin(x*.02))/.25)**2)
c=np.stack([20+22*a+65*marks,44+40*a+65*marks,77+55*a+50*marks],axis=-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'indigo-color.png')
Image.fromarray(np.uint8(np.clip(145+15*n+18*np.sin(x*.04),0,255))).save(R/'indigo-roughness.png')
s=np.clip(47+12*n+10*np.sin(x*.09+np.sin(y*.07)),15,100)
Image.fromarray(np.uint8(np.stack([s*.92,s,s*1.02],axis=-1))).save(R/'volcanic.png')
print('MAPS PASS')
