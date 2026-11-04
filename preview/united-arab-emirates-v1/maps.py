from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];rng=np.random.default_rng(521)
c=np.zeros((512,512,3))+[126,29,29]
for center,width,color in [(100,10,[224,200,153]),(118,6,[28,24,22]),(140,4,[224,200,153]),(340,10,[224,200,153]),(360,6,[28,24,22]),(380,4,[224,200,153])]:c[abs(y-center)<width]=color
weave=.92+.055*np.sin(x*np.pi/2)+.035*np.sin(y*np.pi/2)+rng.normal(0,.012,x.shape)
Image.fromarray(np.uint8(np.clip(c*weave[:,:,None],0,255))).save(R/'weave-color.png')
Image.fromarray(np.uint8(170+35*(.5+.5*np.sin(x*np.pi/2)*np.sin(y*np.pi/2)))).save(R/'weave-roughness.png')
Image.new('RGB',(32,32),(40,28,23)).save(R/'weave-end.png')
s=np.clip(rng.normal(65,9,(128,128)),30,100).astype('uint8');Image.fromarray(np.stack([s,s,s],-1)).save(R/'granite.png')
print('PASS procedural textile maps')
