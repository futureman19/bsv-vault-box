"""Original procedural stone maps. No photographic or museum image inputs."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521)
y,x=np.mgrid[0:512,0:512]/512
warp=y+.045*np.sin(x*9+y*5)+.014*np.sin(x*27-y*12)+.005*np.sin(x*70+y*30)
bands=(.5+.5*np.sin(warp*90+2*np.sin(warp*24)))**7
fine=(.5+.5*np.sin(warp*340+x*3))**18
noise=rng.normal(0,1.4,x.shape)
cream=np.array([221,203,165]);honey=np.array([167,123,66])
t=np.clip(.64*bands+.17*fine,0,1)
color=cream[None,None,:]*(1-t[:,:,None])+honey[None,None,:]*t[:,:,None]+noise[:,:,None]
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'alabaster-color.png')
rough=np.uint8(np.clip(105+bands*22+noise*2,0,255));Image.fromarray(rough).save(R/'alabaster-roughness.png')
grain=rng.normal(0,4,(256,256));yy,xx=np.mgrid[0:256,0:256]
stone=np.array([202,177,132])[None,None,:]+grain[:,:,None]+(3*np.sin(yy/9+np.sin(xx/20)))[:,:,None]
Image.fromarray(np.uint8(np.clip(stone,0,255))).save(R/'limestone.png')
print('MAPS PASS: 3 original portable maps')
