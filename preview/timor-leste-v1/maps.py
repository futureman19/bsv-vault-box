from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512];rng=np.random.default_rng(1688)
# Original abstract bands, not copied clan motifs.
palette=np.array([[135,43,32],[27,40,65],[213,190,141],[147,65,40]])
bands=np.zeros((512,512),int)
for lo,hi,c in [(45,74,1),(74,82,2),(82,110,1),(173,181,2),(181,208,1),(208,216,2),(296,304,2),(304,331,1),(331,339,2),(402,430,1),(430,438,2),(438,467,1)]:bands[(y>=lo)&(y<hi)]=c
# Interrupted narrow pale yarn dashes, deliberately nonrepresentational.
bands[((y%64)<4)&((x%32)<19)]=2
weave=(np.sin(x*np.pi)*0+((x%4)<2)*6-3)+((y%4)<2)*5-2
noise=rng.normal(0,1.6,(512,512))
a=np.clip(palette[bands]+weave[...,None]+noise[...,None],0,255).astype('uint8');Image.fromarray(a).save(R/'textile.png')
r=np.clip(210+weave*2+noise,0,255).astype('uint8');Image.fromarray(r).convert('RGB').save(R/'roughness.png')
g=8*np.sin(y*.16+np.sin(x*.024))+3*np.sin(y*.75+x*.006)+rng.normal(0,1,(512,512))
a=np.clip(np.array([81,43,24])+g[...,None],0,255).astype('uint8');Image.fromarray(a).save(R/'wood.png')
print('MAPS PASS: three original 512px maps')
