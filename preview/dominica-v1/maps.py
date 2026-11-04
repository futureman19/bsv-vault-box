from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(814);n=256
y,x=np.mgrid[:n,:n];grain=rng.normal(0,1,(n,n));cloud=np.sin(x*.055+np.sin(y*.045))*np.cos(y*.06)+.3*np.sin(x*.17+y*.11)
stone=np.clip(np.array([52,61,59])+cloud[:,:,None]*7+grain[:,:,None]*5,0,255).astype('uint8');Image.fromarray(stone).save(R/'stone-color.png')
rough=np.clip(196+grain*11+cloud*8,120,240).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'stone-roughness.png')
f=np.clip(np.array([42,91,46])+cloud[:,:,None]*np.array([10,20,9])+grain[:,:,None]*6,0,255).astype('uint8');Image.fromarray(f).save(R/'forest-color.png')
print('MAPS PASS')
