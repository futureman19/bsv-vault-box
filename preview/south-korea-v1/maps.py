from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:256,0:256];q=(np.sin(x*.045+np.sin(y*.07))+np.sin(y*.043+x*.017))/2
for name,a in [('lacquer',np.stack([12+q*3,22+q*4,25+q*4],-1)),('roughness',np.repeat((63+q*12)[...,None],3,axis=2)),('pearl',np.stack([186+q*29,207+np.sin(x*.065+y*.02)*22,211+np.cos(y*.06-x*.025)*29],-1))]:Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/(name+'.png'))
print('MAPS PASS')
