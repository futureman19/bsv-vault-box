from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1622);y,x=np.mgrid[:256,:512]
f=np.sin(x*.7+2*np.sin(y*.08))+ .4*np.sin(x*1.7+y*.03)+rng.normal(0,.3,x.shape)
base=np.stack([155+f*12,127+f*10,67+f*7],axis=-1)
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'cedar-color.png')
Image.fromarray(np.uint8(np.clip(168+f*16,0,255))).save(R/'cedar-roughness.png')
Image.fromarray(np.uint8(np.clip(base*.7,0,255))).save(R/'cedar-end.png')
f=rng.normal(0,25,(256,256));a=np.stack([90+f,85+f,62+f],axis=-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'granite.png')
