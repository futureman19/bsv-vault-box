"""Independently generated porous ochre sandstone maps; no research imagery."""
from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1336);n=512
y,x=np.mgrid[:n,:n]/n
# Broad mottling under fine pores; deliberately no Japanese wood grain.
field=.6*np.sin(19*x+3*np.sin(11*y))+.35*np.sin(27*y-5*x)+.22*np.cos(61*x+31*y)
grain=rng.normal(0,1,(n,n));pores=rng.random((n,n))<.035
rgb=np.array([184,132,72])[None,None,:]+field[:,:,None]*np.array([15,12,8])+grain[:,:,None]*3-pores[:,:,None]*np.array([26,20,13])
Image.fromarray(np.clip(rgb,0,255).astype('uint8')).save(R/'sand-color.png')
rough=np.clip(205+grain*7+pores*15,0,255).astype('uint8');Image.fromarray(rough).save(R/'sand-roughness.png')
height=field*.02+grain*.007-pores*.04;dy,dx=np.gradient(height)
normal=np.stack([-dx*4,-dy*4,np.ones_like(dx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.clip((normal*.5+.5)*255,0,255).astype('uint8')).save(R/'sand-normal.png')
print('MAPS PASS: 3 generated 512x512 maps')
