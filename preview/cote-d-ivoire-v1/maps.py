from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:256,:256];rng=np.random.default_rng(1949)
weave=1+.07*np.sin(x*np.pi/2)+.06*np.sin(y*np.pi/2)+rng.normal(0,.018,x.shape)
for name,c in [('indigo',(36,59,98)),('cream',(222,211,174)),('ochre',(186,135,58)),('walnut',(57,39,29))]:
 a=np.clip(np.array(c)[None,None,:]*weave[:,:,None],0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
Image.fromarray(np.uint8(180+25*np.sin(x*np.pi/2)*np.cos(y*np.pi/2))).save(R/'weave-roughness.png')
print('MAPS PASS')
