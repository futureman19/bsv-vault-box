from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(821);y,x=np.mgrid[:512,:512];noise=rng.normal(0,2,(512,512));fiber=3*np.sin(x*2.1)+2*np.sin(y*.3+x*.04)
base=np.array([205,170,114])[None,None,:]+(noise+fiber)[:,:,None]
u=(x%128)/128;v=(y%128)/128;d=abs(u-.5)+abs(v-.5)
pattern=(abs(d-.37)<.035)|(abs(d-.22)<.022)|(x%128<5)|(y%128<5)
color=base.copy();color[pattern]=np.array([100,55,30])+noise[pattern,None]
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'ngatu-color.png')
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'fiber-color.png')
Image.fromarray(np.uint8(np.clip(210+noise*3+fiber,0,255))).save(R/'ngatu-roughness.png')
print('MAPS PASS')
