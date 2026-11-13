from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1060);y,x=np.mgrid[0:512,0:512]
noise=rng.normal(0,1,(512,512));field=5*np.sin(x*.031+np.sin(y*.043)*2)+3*np.sin(y*.079)+noise*6
for name,base in [('volcanic-color',(81,67,53)),('ochre-color',(151,119,66))]:
 a=np.stack([np.clip(c+field,0,255) for c in base],axis=-1).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
Image.fromarray(np.clip(204+noise*15,0,255).astype('uint8')).save(R/'stone-roughness.png')
print('MAPS PASS')
