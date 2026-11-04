from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(700);y,x=np.mgrid[:256,:256];n=rng.normal(0,5,(256,256));cloud=5*np.sin(x*.036+np.sin(y*.05))*np.cos(y*.024)
fleck=rng.random((256,256))<.045
for name,color in [('limestone',(217,200,167)),('sand',(230,183,173))]:
 a=np.array(color)[None,None,:]+(n+cloud)[:,:,None];a[fleck]-=np.array([10,22,23]);Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/(name+'.png'),optimize=True)
Image.fromarray(np.uint8(np.clip(185+n*2+cloud,100,240))).save(R/'roughness.png',optimize=True)
print('MAPS PASS: three procedural 256px maps')
