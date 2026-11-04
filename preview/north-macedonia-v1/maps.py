from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(724);y,x=np.mgrid[:256,:256];n=rng.normal(0,2,(256,256));v=5*np.sin(x*.09+np.sin(y*.07)*2)+3*np.cos(y*.17+x*.05)+n
Image.fromarray(np.uint8(np.clip(np.array([192,183,158])+v[:,:,None],0,255))).save(R/'stone-color.png')
Image.fromarray(np.uint8(np.clip(180+v*2,0,255))).convert('RGB').save(R/'stone-roughness.png')
v=3*np.sin(x*.08+y*.11)+rng.normal(0,.8,(256,256));Image.fromarray(np.uint8(np.clip(np.array([25,115,153])+v[:,:,None],0,255))).save(R/'lake-color.png')
print('MAPS PASS')
