from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps'; R.mkdir(exist_ok=True)
rng=np.random.default_rng(812); y,x=np.mgrid[0:512,0:512]/512
v=np.zeros((512,512))
for size,amp in [(7,.14),(19,.075),(51,.035)]:
 noise=Image.fromarray(np.float32(rng.normal(0,1,(size,size))),mode='F').resize((512,512),Image.Resampling.BICUBIC)
 v+=np.asarray(noise)*amp
v+=rng.normal(0,.012,x.shape)
a=np.stack([133+v*160,129+v*150,124+v*140],-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'stone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(176+v*140,0,255))).save(R/'stone-roughness.png',optimize=True)
n=rng.normal(0,20,(256,256)); a=np.stack([114+n,110+n,104+n],-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'mineral.png',optimize=True)
print('PASS procedural maps')
