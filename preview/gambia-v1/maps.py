from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);y,x=np.mgrid[0:512,0:512]/512
warp=y+.045*np.sin(x*19)+.018*np.sin(x*43+y*7)
trace=np.exp(-((np.sin(warp*68))/.13)**2)
fine=rng.normal(0,2,x.shape)
base=np.array([152,112,68]);rgb=base[None,None,:]+(9*np.sin(warp*28)-trace*28+fine)[:,:,None]
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'sediment-color.png')
Image.fromarray(np.uint8(np.clip(153+trace*35+fine*2,0,255))).save(R/'sediment-roughness.png')
rgb=np.array([126,105,67])[None,None,:]+(rng.normal(0,7,(256,256))+np.sin(np.arange(256)[None,:]/9)*5)[:,:,None]
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'silt-color.png')
print('MAPS PASS')
