from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512]/512
u=(x*2)%1-.5;v=(y*2)%1-.5;r=np.hypot(u,v);a=np.arctan2(v,u)
petal=.22+.10*np.cos(8*a)
col=np.zeros((512,512,3))+[230,223,205]
col[(r<petal)&(r>.10)]=[23,75,131]
col[(r<petal-.027)&(r>.15)]=[49,163,172]
col[(r<.075)]=[23,75,131]
col[(r>.41)&(r<.43)]=[49,163,172]
rng=np.random.default_rng(521);noise=rng.normal(0,.8,(512,512,1))
Image.fromarray(np.uint8(np.clip(col+noise,0,255))).save(R/'ceramic-color.png',optimize=True)
Image.fromarray(np.uint8(72+12*np.sin(x*24)*np.sin(y*19)+rng.random((512,512))*4)).save(R/'ceramic-roughness.png',optimize=True)
v=rng.normal(1,.025,(128,128,1));Image.fromarray(np.uint8(np.clip(v*np.array([158,85,52]),0,255))).save(R/'clay.png',optimize=True)
print('MAPS PASS')
