from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(981); y,x=np.mgrid[:256,:512];noise=rng.normal(0,2,(256,512)); pores=rng.random((256,512))<.045
v=4*np.sin(x/37+y/23)+noise-pores*rng.uniform(10,37,(256,512))
a=np.clip(np.array([206,195,164])[None,None,:]+v[:,:,None],0,255).astype('uint8')
Image.fromarray(a).save(R/'tufa-color.png')
Image.fromarray(np.clip(195+v,0,255).astype('uint8')).save(R/'tufa-roughness.png')
Image.fromarray(np.clip(a*.63,0,255).astype('uint8')).save(R/'stone-foot.png')
print('MAPS PASS')
