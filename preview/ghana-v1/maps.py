from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:256];u=x/256;v=y/512
palette=np.array([[212,154,40],[168,50,37],[35,88,73],[25,28,25]])
# Original geometric strip: stepped diamonds alternate with ladder-like bars.
row=y//64;d=np.abs(u-.5)*2+np.abs((y%128)/64-1)
idx=np.where(d<.65,1,np.where(d<.92,3,0))
idx=np.where((row%2==1)&((y%16)<7),2,idx)
idx=np.where((x<18)|(x>237),3,idx)
idx=np.where(((x>22)&(x<29))|((x>226)&(x<233)),2,idx)
weave=((x%4==0)*-9+(y%4==0)*7)[...,None]
Image.fromarray(np.uint8(np.clip(palette[idx]+weave,0,255))).save(R/'kente-color.png')
Image.fromarray(np.uint8(175+(x%4)*8+(y%4)*3)).save(R/'kente-roughness.png')
y,x=np.mgrid[:256,:512];grain=8*np.sin(y*.9+2*np.sin(x*.025))+5*np.sin(y*2.1+x*.013)
wood=np.clip(np.array([75,44,28])+grain[...,None],0,255).astype('uint8')
Image.fromarray(wood).save(R/'wood-color.png')
print('MAPS PASS: original 256x512 textile, roughness, 512x256 wood')
