from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(604);y,x=np.mgrid[0:384,0:512];u=x/512;v=y/384
w=v+.028*np.sin(u*2*np.pi)+.018*np.sin(u*6*np.pi+v*8)+.009*np.sin(u*14*np.pi+v*17)
w+=.04*np.exp(-((u-.65)/.13)**2)*np.sin(v*21+u*13)
palette=np.array([[143,69,46],[183,100,68],[203,136,91],[221,177,127],[152,86,58],[184,111,84],[218,165,119],[116,73,51]])
edges=np.cumsum(rng.uniform(.006,.065,45));edges=edges/edges[-1]*1.3-.15
c=np.zeros((*w.shape,3));c[:]=palette[0]
for i,e in enumerate(edges):
 blend=np.clip((w-e)/.004,0,1)[...,None];c=c*(1-blend)+palette[i%len(palette)]*blend
grain=rng.normal(0,1,w.shape);fleck=rng.random(w.shape)>.985
c+=grain[...,None]*2.5+fleck[...,None]*18
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'rose-stone.png')
Image.fromarray(np.uint8(np.clip(121+grain*4+fleck*12,90,150))).save(R/'stone-roughness.png')
normal=np.stack([128+grain*5,128+rng.normal(0,5,w.shape),np.full(w.shape,254)],axis=-1)
Image.fromarray(np.uint8(np.clip(normal,0,255))).save(R/'stone-normal.png')
y,x=np.mgrid[0:256,0:512];u=x/512;v=y/256
g=np.sin(v*840+1.2*np.sin(u*8)+.6*np.sin(u*27))+.35*np.sin(v*1330+np.sin(u*13))
c=np.array([48,25,14])+g[...,None]*np.array([3,2,1])+rng.normal(0,.65,(256,512,1));Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'cedar-color.png')
Image.fromarray(np.uint8(np.clip(79+g*4,65,95))).save(R/'cedar-roughness.png')
y,x=np.mgrid[0:256,0:256];n=rng.normal(0,1,(256,256));c=np.array([165,100,70])+n[...,None]*8+np.sin(x*.18+y*.09)[...,None]*7;Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'atlas-rock.png')
print('6 compact generated maps; not scans')
