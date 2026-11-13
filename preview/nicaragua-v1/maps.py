from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(417);y,x=np.mgrid[:256,:256];grain=rng.normal(0,7,(256,256));field=6*np.sin(x*.09+np.sin(y*.07))+3*np.sin(y*.13+x*.11)
a=np.stack([55+grain+field,62+grain+field,63+grain+field],axis=-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'stone-color.png')
r=np.uint8(np.clip(194+grain*2,130,235));Image.fromarray(np.repeat(r[:,:,None],3,2)).save(R/'stone-roughness.png')
w=3*np.sin(x*.12+y*.035)+rng.normal(0,1,(256,256));a=np.stack([18+w,102+w,125+w],axis=-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'lake-color.png')
print('PROCEDURAL_MAPS PASS')
