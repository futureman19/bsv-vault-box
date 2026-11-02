from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(701);y,x=np.mgrid[0:256,0:512]
n=rng.normal(0,1,x.shape);v=7*np.sin(y*.13+2*np.sin(x*.014))+3*np.sin(y*.7+x*.03)+n*3
rgb=np.stack([87+v,59+v*.8,41+v*.55],-1).clip(0,255).astype('uint8')
Image.fromarray(rgb).save(R/'sediment.png')
Image.fromarray((175+n*9+v).clip(0,255).astype('uint8')).save(R/'roughness.png')
Image.fromarray(np.stack([130+n*13,109+n*11,72+n*8],-1).clip(0,255).astype('uint8')).save(R/'sand.png')
print('MAPS PASS')
