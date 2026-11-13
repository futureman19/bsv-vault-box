"""Original deterministic basalt maps, not scans or source photographs."""
from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(224004); y,x=np.mgrid[0:256,0:512]
f=.5*np.sin(x*.033+np.sin(y*.054)*1.8)+.3*np.sin(y*.073-x*.026)+.2*np.sin(x*.13+y*.17)
pore=rng.normal(0,1,x.shape);v=np.clip(60+14*f+4*pore,38,85)
Image.fromarray(np.uint8(np.stack([v,v*.99,v*.94],-1))).save(R/'basalt-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(188+15*f+5*pore,166,217))).save(R/'basalt-roughness.png',optimize=True)
gy,gx=np.gradient(f+.05*pore);n=np.stack([-gx*.3,-gy*.3,np.ones_like(f)],-1);n/=np.linalg.norm(n,axis=-1)[...,None]
Image.fromarray(np.uint8(np.clip((n*.5+.5)*255,0,255))).save(R/'basalt-normal.png',optimize=True)
print('PASS procedural basalt color/roughness/normal maps 512x256')
