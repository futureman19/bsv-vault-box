from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(670);y,x=np.mgrid[:256,:512];u=x/512;v=y/256
field=5*np.sin(u*37+3*np.sin(v*13))+4*np.sin(v*35+u*15)+rng.normal(0,2,x.shape)
vein=np.exp(-((np.sin(u*24+v*13+0.6*np.sin(v*22)))/.055)**2)*19
base=np.clip(194+field-vein,145,218)
Image.fromarray(np.uint8(np.stack([base,base+3,base-5],-1))).save(R/'limestone-color.png')
Image.fromarray(np.uint8(np.clip(185+field*.9+vein,150,230))).save(R/'limestone-roughness.png')
Image.fromarray(np.uint8(np.stack([base*.28,base*.62,base*.40],-1))).save(R/'bank-green.png')
print('MAPS PASS')
