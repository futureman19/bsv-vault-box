from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);y,x=np.mgrid[:512,:512]
# Asymmetrical original diamonds, interrupted bands and fine woven fibers.
u=x/64;v=y/64
row=(y//64);offset=np.array([0,.23,.1,.4,.12,.32,.04,.28])[row]
d=np.abs(((u+offset)%1)-.5)+np.abs((v%1)-.5)
pattern=(np.abs(d-.54)<.065)|(np.abs(d-.27)<.043)
pattern &= ~(((x//64+row)%5==0)&((y%64)<20))
base=np.where(pattern[...,None],np.array([50,39,29]),np.array([179,133,75])).astype(float)
weave=4*np.sin(x*np.pi/2)+3*np.cos(y*np.pi/2)+rng.normal(0,1.7,(512,512))
base+=weave[...,None];base+=8*np.sin(y/70)[...,None]
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'raffia-color.png',optimize=True)
rough=np.uint8(np.clip(200+weave*1.5,0,255));Image.fromarray(rough).save(R/'raffia-roughness.png',optimize=True)
n=np.zeros((512,512,3),dtype=np.uint8);n[:,:,0]=128+np.int16(6*np.cos(x*np.pi/2));n[:,:,1]=128+np.int16(6*np.sin(y*np.pi/2));n[:,:,2]=254
Image.fromarray(n).save(R/'raffia-normal.png',optimize=True)
print('MAPS PASS: original 512x512 color/roughness/normal')
