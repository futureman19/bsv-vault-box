from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512]/512
weave=.9+.10*np.sin(x*256*np.pi)*np.sin(y*256*np.pi)
a=(x*6+y*4)%1;b=(x*6-y*4)%1
gold=(np.minimum(a,1-a)<.033)|(np.minimum(b,1-b)<.033)
c=np.stack([110*weave,20*weave,38*weave],-1);c[gold]=np.stack([195*weave,146*weave,65*weave],-1)[gold]
Image.fromarray(c.astype('uint8')).save(R/'songket-color.png')
Image.fromarray(np.uint8(160+30*weave-65*gold)).save(R/'songket-roughness.png')
Image.fromarray(np.uint8(np.stack([50*weave,12*weave,23*weave],-1))).resize((256,256)).save(R/'lining.png')
print('MAPS PASS')
