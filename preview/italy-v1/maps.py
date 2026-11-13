from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512]/512
rng=np.random.default_rng(1568)
f=x+.23*y+.035*np.sin(y*19)+.016*np.sin(y*43+x*11)
v=np.exp(-(np.sin(f*19+.8*np.sin(y*8))/.055)**2)
v2=np.exp(-(np.sin((x-.42*y+.025*np.sin(y*31))*31)/.028)**2)
cloud=np.sin(x*23+y*14)*np.sin(y*17-x*8)
noise=rng.normal(0,1,(512,512))
for name,color,depth in [('ivory',(220,216,203),90),('green',(40,66,53),19),('terracotta',(165,76,49),36)]:
 a=np.clip(np.array(color)[None,None,:]-(v+.3*v2)[:,:,None]*depth+cloud[:,:,None]*5+noise[:,:,None],0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
r=np.clip(105+v*45+cloud*8,0,255).astype('uint8');Image.fromarray(r).save(R/'roughness.png')
print('MAPS PASS 4 generated 512x512 images')
