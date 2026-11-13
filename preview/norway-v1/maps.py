from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(941);y,x=np.mgrid[0:512,0:512]/512
phase=y*18+.8*np.sin(x*8+y*3)+.25*np.sin(x*23+y*7)
band=(.5+.5*np.sin(phase*6.283))**8
v=.83+.36*band+.06*np.sin(y*77+x*11)+rng.normal(0,.018,x.shape)
col=np.stack([84*v,98*v,106*v],-1)
Image.fromarray(np.uint8(np.clip(col,0,255))).save(R/'gneiss-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(170+band*40,0,255))).save(R/'gneiss-roughness.png',optimize=True)
n=rng.normal(0,13,(256,256));c=np.stack([108+n,119+n,122+n],-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'cliff.png',optimize=True)
print('MAPS PASS')
