from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];rng=np.random.default_rng(37)
# Original invented bands/diamonds; not copied traditional tribal symbols.
a=np.empty((512,512,3),dtype=float);a[:]=[143,41,37]
v=y/512;phase=(x%64)/64;diamond=np.abs(phase-.5)*2
for lo,hi in [(.12,.29),(.60,.77)]:
 mask=(v>=lo)&(v<hi);a[mask]=[41,35,34]
 d=diamond+np.abs((v-(lo+hi)/2)/((hi-lo)/2))
 a[mask&(d<.83)]=[213,191,146]
 a[mask&(d<.35)]=[143,41,37]
for v0 in [.08,.33,.56,.81]:a[(v>v0)&(v<v0+.018)]=[213,191,146]
weave=3*np.sin(x*np.pi)+4*np.cos(y*np.pi/2)+rng.normal(0,1.4,(512,512))
a=np.clip(a+weave[...,None],0,255).astype('uint8');Image.fromarray(a).save(R/'sadu-color.png')
r=np.clip(218+9*np.cos(x*np.pi/2)+rng.normal(0,2,(512,512)),0,255).astype('uint8');Image.fromarray(r).save(R/'sadu-roughness.png')
w=np.empty_like(a,dtype=float);grain=8*np.sin(y*.31+2*np.sin(x*.009))+3*np.sin(y*1.3)+rng.normal(0,1,(512,512))
w[:]=[67,41,28];w=np.clip(w+grain[...,None],0,255).astype('uint8');Image.fromarray(w).save(R/'wood-color.png')
s=np.empty((256,256,3),dtype=float);s[:]=[198,165,116];noise=np.random.default_rng(8).normal(0,3,(256,256));s=np.clip(s+noise[...,None],0,255).astype('uint8');Image.fromarray(s).save(R/'sand-color.png')
print('MAPS PASS: four generated maps, maximum 512px')
