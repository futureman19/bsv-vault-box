from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
# Actual browser canvas pixels: inspect object region, not fireworks or UI.
a=np.array(Image.open(R/'hero-fireworks.png').convert('RGB')).astype(float)
h,w=a.shape[:2];crop=a[int(h*.47):int(h*.93),int(w*.32):int(w*.75)]
r,g,b=crop[:,:,0],crop[:,:,1],crop[:,:,2]
mask=(r>170)&(r>g*1.7)&(r>b*1.7)
assert mask.sum()>1000
out=dict(PASS=True,source='hero-fireworks.png',red_pixels=int(mask.sum()),median_actual_red_RGB=np.median(crop[mask],axis=0).tolist(),red_channel_minimum=170,red_over_green_and_blue_ratio_minimum=1.7,scope='actual screenshot object region; highlights can be coral, not exact albedo')
(R/'rendered-color-check.json').write_text(json.dumps(out,indent=2));print(out)
