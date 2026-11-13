from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1359);n=rng.normal(0,7,(256,256));flecks=rng.random((256,256))<.035
base=np.array([197,180,146])[None,None,:]+n[:,:,None];base[flecks]-=28
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'sand-color.png')
Image.fromarray(np.uint8(np.clip(182+n*1.2,0,255))).save(R/'sand-roughness.png')
Image.fromarray(np.uint8(np.clip(base*.82,0,255))).save(R/'mineral.png')
print('MAPS PASS: generated 256px mineral color / roughness')
