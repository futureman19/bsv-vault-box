from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
a=np.array(Image.open(R/'maps/siapo-color.png').convert('RGB')).astype(float)
palette=[[218,195,154],[111,66,42],[48,36,31],[167,89,54]]
f=[float((np.linalg.norm(a-np.array(c),axis=2)<18).mean()) for c in palette]
assert all(x>.01 for x in f) and f[0]>.35
im=Image.open(R/'poster.png').convert('RGBA');ar=np.array(im);assert (ar[:,:,3]>128).mean()>.05 and np.ptp(ar[:,:,:3])>100
r=dict(status='PASS',palette_rgb=palette,palette_pixel_fractions=f,poster_dimensions=im.size,poster_alpha_coverage=float((ar[:,:,3]>128).mean()))
(R/'palette-check.json').write_text(json.dumps(r,indent=2));print('PALETTE_PASS',r)
