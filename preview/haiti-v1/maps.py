from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(807);n=256
y,x=np.mgrid[:n,:n];height=np.zeros((n,n))
for k in range(240):
 cx,cy=rng.uniform(0,n,2);r=rng.uniform(2,10)
 dx=np.minimum(abs(x-cx),n-abs(x-cx));dy=np.minimum(abs(y-cy),n-abs(y-cy));height+=rng.uniform(-1,1)*np.exp(-(dx*dx+dy*dy)/(r*r))
height/=max(abs(height.min()),abs(height.max()));noise=rng.normal(0,1,(n,n))
color=np.clip(np.array([55,69,79])+height[:,:,None]*18+noise[:,:,None]*1.8,0,255).astype('uint8')
Image.fromarray(color).save(R/'steel-color.png')
rough=np.clip(140+height*27+noise*2,0,255).astype('uint8');Image.fromarray(rough).save(R/'steel-roughness.png')
dy,dx=np.gradient(height);norm=np.stack([-dx*.4,-dy*.4,np.ones_like(dx)],axis=-1);norm/=np.linalg.norm(norm,axis=-1,keepdims=True)
Image.fromarray(np.uint8(np.clip((norm*.5+.5)*255,0,255))).save(R/'steel-normal.png')
print('MAPS PASS: original seeded hammered-steel color, roughness, normal')
