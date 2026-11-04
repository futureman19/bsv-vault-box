from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);y,x=np.mgrid[0:512,0:512]/512
phase=y*115+0.5*np.sin(x*9+y*8)+.16*np.sin(x*21+y*15)
grain=(.5+.5*np.sin(phase*6.283))**12
fine=(.5+.5*np.sin((y*231+.12*np.sin(x*13))*6.283))**10
v=1-.22*grain-.10*fine+.07*np.sin(y*19+x*2)+rng.normal(0,.012,x.shape)
wood=np.stack([155*v,108*v,62*v],-1)
Image.fromarray(np.uint8(np.clip(wood,0,255))).save(R/'wood-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(wood*.68,0,255))).resize((256,256)).save(R/'wood-end.png',optimize=True)
Image.fromarray(np.uint8(np.clip(146+grain*34+fine*20,0,255))).save(R/'wood-roughness.png',optimize=True)
noise=rng.normal(0,1,(256,256));speck=np.clip(104+noise*24,38,177)
Image.fromarray(np.uint8(np.stack([speck*1.03,speck*1.02,speck],-1))).save(R/'granite.png',optimize=True)
print('generated compact portable maps')

y,x=np.mgrid[0:256,0:256]
weave=1+.07*np.sin(x*np.pi/2)*np.cos(y*np.pi/2)+.025*np.sin(y*.31)
color=np.empty((256,256,3));color[:]=[194,181,150]
bands=((y>18)&(y<46))|((y>209)&(y<237));color[bands]=[112,30,36]
Image.fromarray(np.uint8(np.clip(color*weave[:,:,None],0,255))).save(R/'linen-color.png')
Image.fromarray(np.uint8(np.clip(206+22*np.sin(x*np.pi/2)*np.cos(y*np.pi/2),0,255))).save(R/'linen-roughness.png')
