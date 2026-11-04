from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(821);y,x=np.mgrid[:512,:512]/512
p=x*29+.19*np.sin(y*9+x*14)+.07*np.sin(y*31)
g=(.5+.5*np.sin(p*6.283))**9
v=.82-.28*g+.12*np.sin(x*17+y*3)+rng.normal(0,.018,x.shape)
a=np.clip(np.stack([152*v,96*v,68*v],-1),0,255).astype('uint8')
Image.fromarray(a).save(R/'earth-color.png');Image.fromarray(a).resize((256,256)).save(R/'earth-end.png')
Image.fromarray(np.uint8(160+60*g)).save(R/'earth-roughness.png')
n=np.clip(90+rng.normal(0,20,(256,256)),30,160).astype('uint8');Image.fromarray(n).save(R/'granite.png')
print('MAPS PASS')
