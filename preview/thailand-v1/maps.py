from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:256,0:256]/256
rng=np.random.default_rng(764)
v=.55*np.sin(x*19+np.sin(y*13))+.3*np.sin(y*31+x*7)+rng.normal(0,.08,x.shape)
c=np.stack([123+23*v,175+21*v,160+22*v],-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'celadon-color.png')
Image.fromarray(np.uint8(np.clip(c+26,0,255))).save(R/'celadon-pale.png')
Image.fromarray(np.uint8(np.clip(78+18*v,0,255))).save(R/'celadon-roughness.png')
Image.fromarray(np.uint8(np.clip(c*.32,0,255))).save(R/'ceramic-foot.png')
print('PASS procedural 256px celadon maps')
