from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(242);y,x=np.mgrid[0:512,0:512]
fiber=rng.normal(0,1.8,x.shape)+2*np.sin(y*.7)+1.2*np.sin(x*.43)
c=np.zeros((512,512,3))+[218,199,157]
# Invented rectilinear borders, not a traced ceremonial masi design.
row=y%128;col=x%64
mask=((row<8)|(row>119)|((row>23)&(row<104)&((col<7)|(col>56))))
tri=(row>36)&(row<92)&(np.abs(col-32)<(row-36)*.38)
c[mask]=[57,38,25];c[tri]=[132,68,39]
c+=fiber[:,:,None]
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'masi-color.png',optimize=True)
rough=193+fiber*2+mask*17
Image.fromarray(np.uint8(np.clip(rough,0,255))).save(R/'masi-roughness.png',optimize=True)
y,x=np.mgrid[0:256,0:256];v=1+.09*np.sin(y*.7+.6*np.sin(x*.02))+.04*rng.normal(0,1,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([86*v,48*v,27*v],-1),0,255))).save(R/'wood.png',optimize=True)
print('PASS procedural maps: cream/umber/russet, fibrous roughness, dark wood')
