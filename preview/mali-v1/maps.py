from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(516);y,x=np.mgrid[0:256,0:256]
# Isotropic mottled mineral grains and shallow irregular sediment variation.
n=rng.normal(0,4,(256,256));field=7*np.sin(x*.071+np.sin(y*.053))+5*np.sin(y*.09+np.sin(x*.04))+n
rgb=np.clip(np.array([170,112,61])+field[:,:,None]*np.array([1,.85,.6]),0,255).astype('uint8')
Image.fromarray(rgb).save(R/'ochre-color.png')
rough=np.clip(199+field*.8,0,255).astype('uint8');Image.fromarray(rough).save(R/'ochre-roughness.png')
Image.fromarray(np.clip(rgb*.71,0,255).astype('uint8')).save(R/'earth-dark.png')
print('MAPS PASS',rgb.mean(axis=(0,1)).tolist())
