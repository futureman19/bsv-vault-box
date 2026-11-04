from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(120);y,x=np.mgrid[:256,:256]
f=np.sin(y*.30+np.sin(x*.027)*2.1+np.sin(x*.09)*.45)*.5+rng.normal(0,.18,(256,256))
a=np.clip(np.array([78,91,105])+f[:,:,None]*25,0,255).astype('uint8')
Image.fromarray(a).save(R/'slate-color.png')
Image.fromarray(np.clip(195+f*30,0,255).astype('uint8')).save(R/'slate-roughness.png')
Image.fromarray(np.clip(90+rng.normal(0,22,(256,256,1))+np.zeros((256,256,3)),0,255).astype('uint8')).save(R/'granite.png')
print('MAPS PASS')
