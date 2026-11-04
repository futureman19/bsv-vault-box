"""Original digital palm-coil interpretation, not a scan or traditional motif copy."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:1024];u=x/1024;v=y/512
rng=np.random.default_rng(721)
coil=(v*24)%1; stitch=(u*160+np.floor(v*24)*.5)%1
# Bespoke interrupted chevrons; three tones over tightly bound horizontal coils.
chevron=np.abs((u*8)%1-.5)*2
motif=(np.abs((v*4-chevron*.65)%1-.5)<.12)&(v>.12)&(v<.89)
base=np.where(motif[...,None],np.array([80,56,36]),np.array([191,161,106])).astype(float)
light=(.9+.10*np.sin(coil*np.pi))*(.90+.10*np.sin(stitch*np.pi))
base=base*light[...,None]+rng.normal(0,1.3,(512,1024,1))
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'palm-color.png')
height=.12*np.cos(coil*2*np.pi)+.035*np.cos(stitch*2*np.pi)
dy,dx=np.gradient(height);n=np.stack([-dx*3,-dy*3,np.ones_like(dx)],axis=2);n/=np.linalg.norm(n,axis=2)[...,None]
Image.fromarray(np.uint8((n*.5+.5)*255)).save(R/'palm-normal.png')
rough=np.uint8(np.clip(190+18*np.cos(stitch*2*np.pi)+8*np.cos(coil*2*np.pi),0,255))
Image.fromarray(rough).save(R/'palm-roughness.png')
print('MAPS PASS 1024x512 color/normal/roughness')
