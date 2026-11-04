from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1190);y,x=np.mgrid[:256,:256];grain=rng.normal(0,1,(256,256));field=3*np.sin(x*.17)*np.sin(y*.13)+grain*5
color=np.clip(np.array([211,197,160])[None,None,:]+field[:,:,None],0,255).astype('uint8');Image.fromarray(color).save(R/'sand-color.png')
Image.fromarray(np.clip(192+field,0,255).astype('uint8')).save(R/'sand-roughness.png')
dy,dx=np.gradient(field);normal=np.stack([128-dx*.7,128-dy*.7,np.full_like(dx,254)],axis=2);Image.fromarray(np.clip(normal,0,255).astype('uint8')).save(R/'sand-normal.png');print('MAPS PASS')
