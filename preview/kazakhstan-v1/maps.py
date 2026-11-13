from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(998);n=512;y,x=np.mgrid[:n,:n]
grain=rng.normal(0,3,(n,n))+2*np.sin(x*1.3+y*.3)+1.5*np.sin(y*1.9)
color=np.clip(np.array([197,174,130])+grain[:,:,None],0,255).astype('uint8')
Image.fromarray(color).save(R/'felt-color.png')
Image.fromarray(np.clip(233+grain,0,255).astype('uint8')).save(R/'felt-roughness.png')
g=5*np.sin(y*.32+2*np.sin(x*.012))+3*np.sin(y*1.1+np.sin(x*.04))+rng.normal(0,1,(n,n))
Image.fromarray(np.clip(np.array([103,63,36])+g[:,:,None],0,255).astype('uint8')).save(R/'wood-color.png')
print('MAPS PASS: deterministic 512px felt color, roughness, wood color')
