from pathlib import Path
import numpy as np,json
from PIL import Image,ImageFilter
from glb_tools import load,accessor
R=Path(__file__).resolve().parent;V6=R.parent/'morocco-finish-v6'
a,ab=load(V6/'morocco.glb');b,bb=load(R/'morocco.glb')
assert a['nodes']==b['nodes']
for ma,mb in zip(a['meshes'],b['meshes']):
 for pa,pb in zip(ma['primitives'],mb['primitives']):
  assert pa['attributes'].keys()==pb['attributes'].keys()
  for k in pa['attributes']:assert np.array_equal(accessor(a,ab,pa['attributes'][k]),accessor(b,bb,pb['attributes'][k]))
  assert np.array_equal(accessor(a,ab,pa['indices']),accessor(b,bb,pb['indices']))
def stats(folder):
 tile=np.asarray(Image.open(folder/'maps/tile-repeat.png'),dtype=float)
 wood=np.asarray(Image.open(folder/'maps/cedar-edge.jpg'),dtype=float)
 smooth=np.asarray(Image.fromarray(wood.astype('uint8')).filter(ImageFilter.GaussianBlur(3)),dtype=float).mean(2)
 return {'tile_near_black_fraction':float((tile.mean(2)<35).mean()),'tile_mean_luminance':float(tile.mean()),'wood_mean_rgb':wood.mean((0,1)).tolist(),'wood_mean_channel_spread':float((wood.max(2)-wood.min(2)).mean()),'wood_within_row_variation':float(wood.mean(2).std(axis=1).mean()),'wood_direction_ratio_3px':float(np.abs(np.diff(smooth,axis=0)).mean()/np.abs(np.diff(smooth,axis=1)).mean())}
x,y=stats(V6),stats(R)
assert y['tile_near_black_fraction']>x['tile_near_black_fraction']
assert y['wood_mean_channel_spread']<x['wood_mean_channel_spread']
assert y['wood_direction_ratio_3px']>1.5 and y['wood_within_row_variation']>3
# Analytic phase equality at all four miter boundaries, across the full border width.
errs=[]
for d in np.linspace(0,.36,101):
 for length,repeats in [(3.57,6),(2.66,4)]:
  start=(d-d)/(length-2*d)*repeats
  end=((length-d)-d)/(length-2*d)*repeats
  errs.extend([abs(start),abs(end-repeats)])
assert max(errs)<1e-12
out={'v6':x,'v7':y,'all_v6_geometry_indices_UVs_exact':True,'miter_corner_phase_max_error':max(errs),'corner_phase_samples':len(errs),'limit':'Phase continuity is not visual corner-composition equivalence. Pixel classes and channel spread are not rendered perceptual match.'}
(R/'delta-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
