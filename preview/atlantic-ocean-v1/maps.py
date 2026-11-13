from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:256,0:256]/256
v=(np.sin(x*24+np.sin(y*15)*2)+np.sin(y*32+x*8)*.35)/2.7+.5
rgb=np.stack([12+v*15,35+v*40,57+v*52],axis=-1)
Image.fromarray(rgb.astype('uint8')).save(R/'abyss-color.png')
rough=np.uint8(78+v*42);Image.fromarray(rough).convert('RGB').save(R/'abyss-roughness.png')
normal=np.stack([128+np.cos(x*24+np.sin(y*15)*2)*5,128+np.cos(y*32+x*8)*4,np.full_like(x,254)],axis=-1)
Image.fromarray(normal.astype('uint8')).save(R/'abyss-normal.png')
print('MAPS PASS: authored 256px color / roughness / normal')