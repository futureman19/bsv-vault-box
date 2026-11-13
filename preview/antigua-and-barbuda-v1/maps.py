from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(281);y,x=np.mgrid[:256,:256];grain=rng.normal(0,1,x.shape)
v= .95+.025*np.sin(x*.08+np.sin(y*.06))+.025*np.sin(y*.12)+grain*.035
pores=rng.random(x.shape)<.025;v[pores]-=.22
color=np.stack([214*v,201*v,174*v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'limestone-color.png')
Image.fromarray(np.uint8(np.clip(192+grain*12+pores*25,0,255))).save(R/'limestone-roughness.png')
pink=np.stack([218+grain*7,153+grain*7,149+grain*6],-1)
Image.fromarray(np.uint8(np.clip(pink,0,255))).save(R/'shell-sand.png')
print('MAPS PASS')
