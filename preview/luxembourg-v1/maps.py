from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(244);y,x=np.mgrid[:512,:512];grain=rng.normal(0,3,(512,512));layers=5*np.sin(y*.18+np.sin(x*.017)*1.2)+3*np.sin(y*.55+x*.006);v=grain+layers
rgb=np.clip(np.array([190,167,125])+v[:,:,None],0,255).astype('uint8');Image.fromarray(rgb).save(R/'sandstone-color.png')
rough=np.clip(196+grain*2,150,235).astype('uint8');Image.fromarray(rough).save(R/'sandstone-roughness.png')
normal=np.zeros((512,512,3),dtype='uint8');normal[:,:,0]=np.clip(128+grain,0,255);normal[:,:,1]=np.clip(128+np.gradient(v)[0],0,255);normal[:,:,2]=255;Image.fromarray(normal).save(R/'sandstone-normal.png')
print('MAPS PASS')
