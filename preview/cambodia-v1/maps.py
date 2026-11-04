from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(668);n=256
low=np.asarray(Image.fromarray(rng.integers(0,256,(16,16),dtype=np.uint8)).resize((n,n),Image.Resampling.BICUBIC),dtype=float)/255-.5
noise=rng.normal(0,1,(n,n));v=low*24+noise*5
rgb=np.stack([166+v,129+v*.85,87+v*.7],axis=2)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'stone-color.png')
rough=np.uint8(np.clip(203+low*24+noise*5,0,255));Image.fromarray(rough).convert('RGB').save(R/'stone-roughness.png')
Image.fromarray(np.uint8(np.clip(np.stack([92+v,89+v,74+v],axis=2),0,255))).save(R/'foot-color.png')
print('MAPS PASS 3 x 256px authored maps')
