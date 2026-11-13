"""Original deterministic maple and Shield granite maps, not scans."""
from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(2041)
y,x=np.mgrid[0:512,0:512]/512
curl=np.sin(y*190+3*np.sin(x*15)+1.5*np.sin(x*43))
fine=np.sin(y*850+6*np.sin(x*11))
cloud=np.sin(x*13+y*7)*np.sin(y*19-x*5)
a=5*curl+2*fine+6*cloud+rng.normal(0,1.1,x.shape)
col=np.clip(np.array([193,151,94])+a[:,:,None]*np.array([1,.85,.6]),0,255).astype('uint8')
Image.fromarray(col).save(R/'maple-color.png')
rough=np.clip(115+12*curl+4*fine,0,255).astype('uint8');Image.fromarray(rough).save(R/'maple-roughness.png')
y,x=np.mgrid[0:256,0:256]/256
ring=np.sin(np.sqrt((x-.3)**2+(y-.4)**2)*160+np.sin(x*20))
Image.fromarray(np.clip(np.array([155,106,57])+ring[:,:,None]*9,0,255).astype('uint8')).save(R/'maple-end.png')
gr=rng.normal(0,14,x.shape)+9*np.sin(x*55+y*17)*np.sin(y*49)
Image.fromarray(np.clip(np.array([156,135,127])+gr[:,:,None],0,255).astype('uint8')).save(R/'granite.png')
print('MAPS PASS: 512px maple color/roughness; 256px endgrain/granite')
