from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(385);n=rng.normal(0,1,(256,256));coarse=rng.normal(0,1,(32,32));coarse=np.asarray(Image.fromarray(coarse.astype('float32')).resize((256,256),Image.Resampling.BICUBIC))
for name,base in [('earth',[155,83,49]),('stone',[83,72,61])]:
 a=np.clip(np.array(base)[None,None,:]+(n*4+coarse*7)[:,:,None],0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
Image.fromarray(np.clip(195+n*7+coarse*9,0,255).astype('uint8')).save(R/'roughness.png')
