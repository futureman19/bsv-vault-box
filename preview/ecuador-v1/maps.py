from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(729);y,x=np.mgrid[:512,:512];u=(x+y)/10;v=(x-y)/10
fu=u%1;fv=v%1;over=((np.floor(u)+np.floor(v))%2)==0
h=np.where(over,np.sin(np.pi*fu),np.sin(np.pi*fv));groove=np.minimum(fu,1-fu)<.075;groove|=np.minimum(fv,1-fv)<.075
shade=.78+.20*h-.13*groove+rng.normal(0,.014,h.shape)
color=np.clip(shade[...,None]*np.array([228,207,162]),0,255).astype('uint8');Image.fromarray(color).save(R/'straw-color.png')
rough=np.clip(155+35*(1-h)+rng.normal(0,3,h.shape),0,255).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'straw-roughness.png')
dy,dx=np.gradient(h);n=np.stack([-dx*.7,-dy*.7,np.ones_like(h)],axis=-1);n/=np.linalg.norm(n,axis=-1,keepdims=True);Image.fromarray(((n+1)*127.5).astype('uint8')).save(R/'straw-normal.png')
a=rng.normal(0,8,(256,256));c=np.clip(np.array([60,66,63])+a[...,None],0,255).astype('uint8');Image.fromarray(c).save(R/'basalt.png')
print('MAPS_PASS')
