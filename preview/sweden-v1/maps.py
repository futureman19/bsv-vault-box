from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(7521);y,x=np.mgrid[:512,:512]/512
phase=y*93+.34*np.sin(x*12+y*7)
grain=(.5+.5*np.sin(phase*6.283))**12
v=1-.19*grain+.045*np.sin(y*17+x*2)+rng.normal(0,.008,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([145*v,43*v,32*v],-1),0,255))).save(R/'red-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(np.stack([202*v,163*v,112*v],-1),0,255))).resize((256,256)).save(R/'wood-end.png',optimize=True)
Image.fromarray(np.uint8(140+grain*48)).save(R/'wood-roughness.png',optimize=True)
print('PASS generated three compact procedural maps')
