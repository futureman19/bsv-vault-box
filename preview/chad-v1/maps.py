from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1475);y,x=np.mgrid[0:512,0:512]/512
warp=y+.009*np.sin(x*29)+.005*np.sin(x*71+y*12)
# Uneven layer thicknesses, discontinuous fine beds and broad mineral shifts.
profile=rng.normal(0,.55,73)
bands=np.interp(np.clip(warp,0,1),np.linspace(0,1,len(profile)),profile)
bands+=.28*np.sin(x*8+y*19)+.15*np.sin(x*33-y*41)
for level in [.13,.28,.305,.54,.71,.87]:
 bands+=.55*np.exp(-((warp-level)/.003)**2)
grain=rng.normal(0,1,x.shape)
c=np.stack([165+bands*23+grain*3,94+bands*20+grain*3,44+bands*13+grain*2],axis=-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'sandstone-color.png')
Image.fromarray(np.uint8(np.clip(205+bands*8+grain*3,0,255))).convert('RGB').save(R/'sandstone-roughness.png')
Image.fromarray(np.uint8(np.clip(c*.60+grain[...,None]*3,0,255))).save(R/'dark-grain.png')
print('MAPS PASS: three original 512x512 procedural maps')
