from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];rng=np.random.default_rng(96)
thread=5*np.sin(x*np.pi/2)+4*np.sin(y*np.pi/2)+rng.normal(0,1.3,x.shape)
u=(x%64-32)/32;v=(y%64-32)/32
motif=np.abs(np.abs(u)+np.abs(v)-.72)<.055
c=np.zeros((512,512,3))+np.array([90,20,43]);c+=thread[:,:,None];c[motif]=np.array([190,140,62])+thread[motif,None]
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'cedar-color.png')
rough=np.clip(175+thread*3-motif*55,0,255).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'cedar-roughness.png')
Image.fromarray(np.uint8(np.clip(c*.6,0,255))).save(R/'cedar-end.png')
g=rng.integers(36,110,(256,256),dtype=np.uint8);Image.fromarray(g).convert('RGB').save(R/'granite.png')
print('MAPS PASS')
