from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:256,0:256];rng=np.random.default_rng(419)
f=(np.sin(x*.038+np.sin(y*.025)*2)+np.cos(y*.054+x*.012)+np.sin(x*.11-y*.066)*.3)/2.3
noise=rng.normal(0,1,(256,256))
base=np.stack([43+14*f+noise,103+24*f+noise,65+12*f+noise],axis=-1)
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'jade.png')
r=np.uint8(np.clip(82+f*14+noise*2,0,255));Image.fromarray(np.repeat(r[:,:,None],3,axis=2)).save(R/'roughness.png')
b=np.stack([205+f*8,191+f*7,147+f*6],axis=-1);Image.fromarray(np.uint8(b)).save(R/'ivory.png')
print('MAPS PASS')
