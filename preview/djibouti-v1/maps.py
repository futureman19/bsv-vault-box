from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(5959);n=256
y,x=np.mgrid[:n,:n];noise=rng.random((n,n));v=.5+.14*np.sin(x*.061+np.sin(y*.08)*3)+.10*np.sin(y*.17+x*.09)+.14*(noise-.5)
a=np.stack([40+v*43,38+v*37,34+v*30],axis=2).astype('uint8');Image.fromarray(a).save(R/'basalt-color.png')
Image.fromarray((178+noise*45).astype('uint8')).save(R/'basalt-roughness.png')
normal=np.zeros((n,n,3),dtype='uint8');normal[:,:,0]=124+noise*7;normal[:,:,1]=124+rng.random((n,n))*7;normal[:,:,2]=255;Image.fromarray(normal).save(R/'basalt-normal.png')
a=np.stack([218+noise*25,211+noise*26,188+noise*29],axis=2).astype('uint8');Image.fromarray(a).save(R/'salt-color.png')
print('MAPS PASS: four deterministic 256px authored textures')
