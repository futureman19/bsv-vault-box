from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(287);y,x=np.mgrid[0:512,0:512]/512
from PIL import ImageFilter
coarse=np.array(Image.fromarray(np.uint8(rng.uniform(0,255,(32,32)))).resize((512,512),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(3)),dtype=float)/255-.5
flow=np.sin(y*95+5*np.sin(x*13)+coarse*12)*.18+coarse*2
noise=rng.normal(0,1,x.shape);v=flow*25+noise*5
rgb=np.stack([156+v,106+v*.85,53+v*.60],axis=-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'ochre.png',optimize=True)
Image.fromarray(np.uint8(np.clip(195+flow*22+noise*4,0,255))).save(R/'roughness.png',optimize=True)
v=12*np.sin(x*31+y*18)+noise*2
Image.fromarray(np.uint8(np.clip(np.stack([213+v,174+v,111+v],axis=-1),0,255))).save(R/'sand.png',optimize=True)
print('MAPS_PASS')
