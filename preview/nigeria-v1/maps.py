"""Independent resist-circle painting, not museum-image texture extraction."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(901);n=512
y,x=np.mgrid[0:n,0:n]/n
mask=np.zeros((n,n))
for j in range(5):
 for i in range(5):
  cx=(i+.5)/5;cy=(j+.5)/5
  dx=x-cx;dy=y-cy;angle=np.arctan2(dy,dx)
  rad=np.sqrt(dx*dx+dy*dy)
  warped=rad+0.0025*np.sin(angle*7+i+j)+.0015*np.sin(angle*13+j)
  ring=np.exp(-((warped-.063)/.005)**2)+.65*np.exp(-((warped-.048)/.0025)**2)
  dot=np.exp(-(rad/.008)**4)
  mask=np.maximum(mask,np.clip(ring+dot,0,1))
# Paired small resist seeds between the main tied circles.
for j in range(5):
 for i in range(5):
  for ox in [-.014,.014]:
   dx=(x-(i/5+ox)+.5)%1-.5;dy=(y-j/5+.5)%1-.5
   mask=np.maximum(mask,.75*np.exp(-((dx*dx+dy*dy)/.00004)**2))
weave=1.5*np.sin(x*n*np.pi)+1.5*np.cos(y*n*np.pi)
noise=rng.normal(0,1.2,(n,n))+weave
cloud=3*np.sin(x*19+y*11)+2*np.sin(y*37-x*14)
base=np.array([23,54,107]);pale=np.array([185,212,221])
color=np.clip(base+(pale-base)*mask[:,:,None]+noise[:,:,None]+cloud[:,:,None],0,255).astype('uint8')
Image.fromarray(color).save(R/'indigo-color.png')
rough=np.clip(188+noise*2-mask*18,0,255).astype('uint8');Image.fromarray(rough).save(R/'indigo-roughness.png')
h=mask*.03+.006*np.sin(x*n*np.pi/2)+.006*np.sin(y*n*np.pi/2)
gy,gx=np.gradient(h);normal=np.dstack((-gx*5,-gy*5,np.ones_like(h)));normal/=np.linalg.norm(normal,axis=2)[:,:,None]
Image.fromarray(np.clip((normal*.5+.5)*255,0,255).astype('uint8')).save(R/'indigo-normal.png')
print('MAPS_PASS 25 main resist circles, 512x512 color/roughness/normal')
