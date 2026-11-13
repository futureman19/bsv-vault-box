from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);y,x=np.mgrid[0:256,0:512]
grain=np.sin(y*.43+np.sin(x*.021)*1.8)+.4*np.sin(y*1.9+x*.005)+rng.normal(0,.18,x.shape)
t=np.clip((grain+2)/4,0,1)
c=np.stack([33+40*t,23+25*t,17+16*t],axis=-1).astype('uint8')
Image.fromarray(c).save(R/'ebony-color.png')
r=np.clip(104+grain*17,0,255).astype('uint8');Image.fromarray(r).convert('RGB').save(R/'ebony-roughness.png')
s=np.clip(.5+.3*np.sin(x*.09+y*.05)+.2*np.sin(y*.19-x*.03),0,1)
shell=np.stack([226+s*19,217+s*22,193+s*31],axis=-1).astype('uint8');Image.fromarray(shell).save(R/'shell-color.png')
print('MAPS PASS')
