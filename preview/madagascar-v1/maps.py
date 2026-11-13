from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(494);y,x=np.mgrid[0:512,0:512]/512
# Independently generated chalk grain and wandering dissolution traces; no scans.
v=.91+.07*np.sin(y*17+x*13)+.065*np.sin(x*81+np.sin(y*24)*1.8)+rng.normal(0,.023,x.shape)
color=np.stack([170*v,167*v,150*v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'limestone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(195+(1-v)*80,0,255))).save(R/'limestone-roughness.png',optimize=True)
Image.fromarray(np.uint8(np.clip((color-150)*.8+63,0,255))).resize((256,256)).save(R/'cleft-color.png',optimize=True)
print('PASS procedural maps generated')
