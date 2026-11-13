from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(170);y,x=np.mgrid[0:512,0:512]/512
u=(x*6)%1-.5;v=(y*6)%1-.5
# Four almond-like loops in each repeat, original nontraditional motif.
d=np.full(x.shape,10.)
for a in [0,np.pi/2,np.pi,3*np.pi/2]:
 U=u*np.cos(a)+v*np.sin(a);V=-u*np.sin(a)+v*np.cos(a)
 ellipse=((U-.17)/.17)**2+(V/.09)**2
 d=np.minimum(d,np.abs(ellipse-1))
line=d<.15
dots=((u-.42)**2+(v-.42)**2<.0014)|((u+.42)**2+(v+.42)**2<.0014)|(u*u+v*v<.001)
ink=line|dots
noise=rng.normal(0,1.7,x.shape)+1.5*np.sin(x*512*np.pi)+1.5*np.sin(y*512*np.pi)
color=np.where(ink[...,None],np.array([220,198,149]),np.array([28,48,76]))+noise[...,None]
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'batik-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(color*.65,0,255))).resize((256,256)).save(R/'batik-dark.png',optimize=True)
Image.fromarray(np.uint8(np.clip(170+ink*25+noise*2,0,255))).save(R/'batik-roughness.png',optimize=True)
speck=np.clip(60+rng.normal(0,13,(256,256)),20,110)
Image.fromarray(np.uint8(np.stack([speck,speck*1.03,speck*1.1],-1))).save(R/'granite.png',optimize=True)
print('PASS procedural indigo/ivory dots-and-loops maps')
