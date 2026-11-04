from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(619);y,x=np.mgrid[0:512,0:512]/512
u=(x*6)%1-.5;v=(y*4)%1-.5;r=np.sqrt(u*u+v*v);a=np.arctan2(v,u)
petal=(r<(.22+.10*np.cos(a*8)))&(r>.085)
stem=(abs(v-.12*np.sin(u*8))<.014)&(~petal)
color=np.zeros((512,512,3))+[228,222,198]
color[petal]=[24,69,135];color[stem]=[35,131,150];color[r<.065]=[41,151,165]
color+=rng.normal(0,1.4,(512,512,1))
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'floral-color.png',optimize=True)
rough=91+9*np.sin(x*40)*np.sin(y*33)+rng.normal(0,2,x.shape)
Image.fromarray(np.uint8(rough)).save(R/'glaze-roughness.png',optimize=True)
cobalt=np.ones((256,256,3))*[23,58,106]+rng.normal(0,1.2,(256,256,1))
Image.fromarray(np.uint8(cobalt)).save(R/'cobalt-color.png',optimize=True)
stone=100+rng.normal(0,19,(256,256));Image.fromarray(np.uint8(np.clip(np.stack([stone,stone*1.02,stone*1.05],-1),0,255))).save(R/'stone.png',optimize=True)
print('PASS procedural floral/glaze/stone maps')
