"""Deterministic original sand maps, not scans or borrowed photography."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1430);n=512
y,x=np.mgrid[0:n,0:n]/n
wind=np.sin(2*np.pi*(y*46+1.1*np.sin(x*9)+.3*np.sin(x*31)))
broad=np.sin(y*9+x*4)*.035+np.sin(x*17+y*13)*.025
fine=rng.normal(0,.012,(n,n));v=broad+wind*.018+fine
base=np.array([170,84,45]);rgb=np.clip(base[None,None,:]*(1+v[:,:,None])+np.stack([wind*4,wind*2,wind],axis=-1),0,255).astype('uint8')
Image.fromarray(rgb).save(R/'sand-color.png')
rough=np.clip(205+wind*9+fine*150,0,255).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'sand-roughness.png')
# glTF tangent-space normal: very shallow fine aeolian ripple relief.
dy,dx=np.gradient(wind*.18+fine*.3);normal=np.dstack((-dx,-dy,np.ones_like(x)));normal/=np.linalg.norm(normal,axis=2)[:,:,None]
Image.fromarray(np.clip((normal*.5+.5)*255,0,255).astype('uint8')).save(R/'sand-normal.png')
print('MAPS PASS: three deterministic 512x512 original maps')
