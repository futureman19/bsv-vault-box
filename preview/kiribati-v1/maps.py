"""Original generic over/under fibre weave, not a copied Kiribati pattern."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(134416)
h,w=256,512;y,x=np.mgrid[:h,:w];cell=16
u=(x%cell)/cell;v=(y%cell)/cell;vertical=((x//cell+y//cell)%2)==0
across=np.where(vertical,u,v);along=np.where(vertical,y,x)
profile=np.sin(np.pi*np.clip((across-.055)/.89,0,1))**.4
fine=np.sin(across*230+np.sin(along*.07))*1.8
noise=rng.normal(0,1.2,(h,w));shade=profile*26+fine+noise+np.where(vertical,4,-4)
color=np.stack([153+shade*1.65,113+shade*1.55,58+shade*1.35],axis=2)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'pandanus-color.png')
rough=np.uint8(np.clip(192-profile*32+noise*2,0,255));Image.fromarray(rough).save(R/'pandanus-roughness.png')
dy,dx=np.gradient(profile);norm=np.stack([-dx*.7,-dy*.7,np.ones_like(dx)],axis=2);norm/=np.linalg.norm(norm,axis=2,keepdims=True);Image.fromarray(np.uint8((norm*.5+.5)*255)).save(R/'pandanus-normal.png')
y,x=np.mgrid[:128,:256];grain=rng.normal(0,1.7,(128,256));wave=3*np.sin(x*.13+y*.19)
sand=np.stack([218+grain+wave,200+grain+wave,156+grain+wave],2);Image.fromarray(np.uint8(np.clip(sand,0,255))).save(R/'sand-color.png')
print('MAPS PASS: original 512x256 weave colour/roughness/normal, 256x128 sand')
