from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(604);y,x=np.mgrid[0:384,0:512];u=x/512;v=y/384
# Continuous wavy stratification: warm dressed stone, not unrelated noise pixels.
w=v+.025*np.sin(u*13)+.012*np.sin(u*29+v*4)
t=.5+.5*np.sin(w*49+1.7*np.sin(w*11));palette=np.array([[119,57,46],[185,104,78],[204,137,101],[220,178,127],[161,86,62]])
q=t*3.999;ix=q.astype(int);c=palette[ix]*(1-(q-ix)[...,None])+palette[np.minimum(ix+1,4)]*(q-ix)[...,None]
vein=np.exp(-((np.sin(w*86+.4*np.sin(u*22)))/.11)**2);c-=vein[...,None]*26;c+=rng.normal(0,2,(384,512,1));Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'rose-stone.png')
y,x=np.mgrid[0:256,0:512];u=x/512;v=y/256
g=np.sin(v*220+3*np.sin(u*5)+1.3*np.sin(u*21))+ .45*np.sin(v*590+2*np.sin(u*9));c=np.array([65,34,20])+g[...,None]*np.array([8,5,3])+rng.normal(0,1,(256,512,1));Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'cedar-color.png')
rough=np.uint8(np.clip(72+g*8,45,105));Image.fromarray(rough).save(R/'cedar-roughness.png')
y,x=np.mgrid[0:256,0:256];n=rng.normal(0,1,(256,256));c=np.array([173,95,75])+n[...,None]*7+np.sin(x*.18+y*.09)[...,None]*4;Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'atlas-rock.png')
print('4 generated compact maps')
