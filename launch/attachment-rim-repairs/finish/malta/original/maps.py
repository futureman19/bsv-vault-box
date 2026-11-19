from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(73);n=256
y,x=np.mgrid[:n,:n];noise=rng.normal(0,3,(n,n));pores=rng.random((n,n))<.025
shade=noise-pores*24+3*np.sin(x*.07)*np.cos(y*.09)
a=np.clip(np.array([222,197,145])[None,None,:]+shade[:,:,None],0,255).astype('uint8')
Image.fromarray(a).save(R/'limestone-color.png')
rough=np.clip(195+noise*2+pores*25,0,255).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'limestone-roughness.png')
b=np.clip(np.array([31,104,121])[None,None,:]+(3*np.sin(x*.18+y*.09)+noise*.4)[:,:,None],0,255).astype('uint8');Image.fromarray(b).save(R/'harbour-color.png')
print('MAPS PASS')
