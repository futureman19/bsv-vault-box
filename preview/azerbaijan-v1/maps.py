from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(675);n=512;y,x=np.mgrid[:n,:n];h=np.zeros((n,n))
for i in range(900):
 cx,cy=rng.uniform(0,n,2);r=rng.uniform(3,9);dx=np.minimum(abs(x-cx),n-abs(x-cx));dy=np.minimum(abs(y-cy),n-abs(y-cy));h-=rng.uniform(.4,1)*np.exp(-(dx*dx+dy*dy)/(r*r))
h=(h-h.min())/(h.max()-h.min());noise=rng.normal(0,1,(n,n));base=np.array([166,92,55]);rgb=np.clip(base[None,None,:]*(.78+.35*h[:,:,None])+noise[:,:,None]*1.5,0,255).astype('uint8');Image.fromarray(rgb).save(R/'copper-color.png')
rough=np.clip(90+55*h+noise*2,0,255).astype('uint8');Image.fromarray(rough).save(R/'copper-roughness.png')
dy,dx=np.gradient(h);normal=np.dstack((-dx*2,-dy*2,np.ones_like(h)));normal/=np.linalg.norm(normal,axis=2)[:,:,None];Image.fromarray(np.uint8(np.clip((normal*.5+.5)*255,0,255))).save(R/'copper-normal.png')
print('MAPS PASS')
