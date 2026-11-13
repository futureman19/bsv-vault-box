from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(817);y,x=np.mgrid[:256,:512]
f=np.sin(x*.08)*np.sin(y*.11)*5+rng.normal(0,2,(256,512))
for name,c in [('cobalt-color',(23,70,139)),('ochre-color',(198,149,66))]:
 a=np.clip(np.array(c)[None,None,:]+f[:,:,None],0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
a=np.clip(94+f*2,55,140).astype('uint8');Image.fromarray(a).save(R/'glaze-roughness.png')
print('MAPS PASS')
