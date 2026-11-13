from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(506)
coarse=np.asarray(Image.fromarray(np.uint8(rng.uniform(0,255,(32,32)))).resize((512,512),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(3))).astype(float)/255
noise=rng.normal(0,4,(512,512));v=coarse-.5
rgb=np.stack([65+v*55+noise,78+v*65+noise,67+v*45+noise],-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'stone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(rgb*.66,0,255))).resize((256,256)).save(R/'stone-dark.png',optimize=True)
Image.fromarray(np.uint8(np.clip(180+v*65+noise,0,255))).save(R/'stone-roughness.png',optimize=True)
speck=np.clip(75+rng.normal(0,15,(256,256)),20,140)
Image.fromarray(np.uint8(np.stack([speck*.9,speck,speck*.92],-1))).save(R/'granite.png',optimize=True)
print('PASS procedural volcanic maps generated')
