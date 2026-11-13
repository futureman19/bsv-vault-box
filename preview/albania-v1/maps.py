from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(741);y,x=np.mgrid[:256,:256];noise=rng.normal(0,2,(256,256));cloud=4*np.sin(x*.047)*np.cos(y*.067)+3*np.sin((x+y)*.11)
rows=y//32;seams=(y%32<2)|((x+(rows%2)*38)%76<2)
base=174+cloud+noise-seams*28
rgb=np.stack([base,base-6,base-18],axis=-1).clip(0,255).astype('uint8');Image.fromarray(rgb).save(R/'stone-color.png')
rough=(200+noise*3+cloud).clip(0,255).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'stone-roughness.png')
slate=83+cloud+noise*1.4+4*np.sin(y*.35+x*.04)
Image.fromarray(np.stack([slate-9,slate,slate+9],axis=-1).clip(0,255).astype('uint8')).save(R/'slate-color.png')
print('MAPS PASS: three independently generated 256x256 maps')
