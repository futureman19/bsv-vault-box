from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(289)
y,x=np.mgrid[:256,:256]
noise=rng.normal(0,1,(256,256));broad=np.sin(x*.08+np.sin(y*.035))*np.cos(y*.06)
v=1+.065*broad+.08*noise
v-=.32*(rng.random((256,256))>.962)
c=np.stack([186*v,174*v,151*v],-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'granite-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(195+noise*14,120,235))).save(R/'granite-roughness.png',optimize=True)
dy,dx=np.gradient(noise);normal=np.stack([-dx*.05,-dy*.05,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8(np.clip((normal*.5+.5)*255,0,255))).save(R/'granite-normal.png',optimize=True)
print('MAPS PASS: 3 generated 256x256 maps')
