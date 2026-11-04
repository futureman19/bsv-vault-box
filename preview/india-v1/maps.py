from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:256,0:256]/256
phase=x*3+y*1.5+.22*np.sin(y*13+x*3)+.075*np.sin(y*41-x*17)
vein=np.exp(-(np.sin(phase*6.283)/.085)**2)
v=1-.19*vein+.013*np.sin(x*29+y*31)
a=np.stack([225*v,218*v,200*v],-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'marble-color.png')
Image.fromarray(np.uint8(105+vein*39)).save(R/'marble-roughness.png')
print('MAPS PASS')
