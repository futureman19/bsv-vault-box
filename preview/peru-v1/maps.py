from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(274);n=rng.normal(0,1,(256,256)); y,x=np.mgrid[:256,:256]
f=3*np.sin(x*.19+y*.24)+2*np.cos(y*.63-x*.15)+n*5
for name,base in [('stone-color',[137,131,119]),('green-color',[100,118,73])]:
 a=np.clip(np.array(base)[None,None,:]+f[:,:,None],0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
a=np.clip(205+n*9,0,255).astype('uint8');Image.fromarray(a).convert('RGB').save(R/'stone-roughness.png')
print('PASS procedural stone/green/roughness maps')
