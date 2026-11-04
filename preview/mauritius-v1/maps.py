from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(710)
y,x=np.mgrid[0:256,0:512];noise=rng.normal(0,1,x.shape)
f=np.sin(y*.047+1.7*np.sin(x*.018)+.5*np.sin(x*.044+y*.014))
col=np.array([150,86,62])[None,None,:]+f[:,:,None]*np.array([18,13,12])+noise[:,:,None]*3
Image.fromarray(np.uint8(np.clip(col,0,255))).save(R/'earth-color.png')
Image.fromarray(np.uint8(np.clip(195+f*15+noise*5,0,255))).save(R/'earth-roughness.png')
g=np.clip(47+noise*8+7*np.sin(x*.15)*np.sin(y*.17),0,255).astype('uint8')
Image.fromarray(np.stack([g,g+2,g+5],axis=-1)).save(R/'basalt.png')
print('MAPS PASS')
