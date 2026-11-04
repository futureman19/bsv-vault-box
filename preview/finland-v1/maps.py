from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(442);n=512
y,x=np.mgrid[:n,:n];noise=rng.normal(0,2,(n,n));grain=3*np.sin(y*.25+np.sin(x*.018))+2*np.sin(y*.8+x*.004)
b=np.clip(np.array([217,214,199])[None,None,:]+(noise+grain)[...,None],0,255).astype('uint8');im=Image.fromarray(b);d=ImageDraw.Draw(im)
for i in range(210):
 xx=int(rng.integers(-10,512)); yy=int(rng.integers(0,512));w=int(rng.integers(3,30));h=int(rng.integers(1,4));c=int(rng.integers(50,145));d.rounded_rectangle((xx,yy,xx+w,yy+h),radius=1,fill=(c,c,c-7))
im.save(R/'birch-color.png')
wood=np.clip(np.array([202,176,128])[None,None,:]+(grain+noise*.4)[...,None]*2,0,255).astype('uint8');Image.fromarray(wood).save(R/'wood-color.png')
a=np.clip(175+grain*3+noise*2,80,225).astype('uint8');Image.fromarray(a).convert('RGB').save(R/'birch-roughness.png')
a=np.clip(130+15*np.sin(np.sqrt((x-230)**2+(y-280)**2)*.35)+noise*2,0,255);Image.fromarray(np.stack([a+20,a,a-25],2).astype('uint8')).save(R/'birch-end.png')
a=np.clip(110+rng.normal(0,28,(256,256)),35,220).astype('uint8');Image.fromarray(np.stack([a,a,a],2)).save(R/'granite.png')
print('MAPS PASS')
