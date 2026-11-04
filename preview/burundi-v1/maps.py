from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent; (R/'maps').mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512];u=x/512;v=y/512
# Original diamond band, with woven over-under light response and tiny fibres.
phase=np.abs((u*6)%1-.5)*2
band=(v>.22)&(v<.78)
diamond=(np.abs(v-.5)*3.4+phase)<.94
inner=(np.abs(v-.5)*3.4+phase)<.48
base=np.zeros((512,512,3))+[199,164,107]
base[band&diamond]=[53,43,37];base[band&inner]=[144,74,53]
base[(abs(v-.15)<.018)|(abs(v-.85)<.018)]=[144,74,53]
warp=np.sin(x*np.pi/4);weft=np.sin(y*np.pi/3)
relief=(warp*(.5+.5*np.cos(y*np.pi/6))+weft*.45)
fibre=np.sin(x*2.2+y*.12)*1.6+np.random.default_rng(521).normal(0,1,(512,512))
Image.fromarray(np.uint8(np.clip(base+relief[:,:,None]*7+fibre[:,:,None],0,255))).save(R/'maps/sisal-color.png')
Image.fromarray(np.uint8(np.clip(210+relief*12,0,255))).save(R/'maps/sisal-roughness.png')
dy,dx=np.gradient(relief);normal=np.stack([-dx*.13,-dy*.13,np.ones_like(dx)],axis=2);normal/=np.linalg.norm(normal,axis=2)[:,:,None]
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'maps/sisal-normal.png')
print('MAPS_PASS 512x512 color/roughness/normal')
