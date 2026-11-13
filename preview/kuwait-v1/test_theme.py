from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent

def pattern(a):
 assert a.shape==(512,512,3)
 # Explicit palette, chromatic coverage and rhythmic diamond cross-sections.
 targets=[[143,41,37],[41,35,34],[213,191,146]]
 fractions=[float((np.max(abs(a.astype(float)-c),axis=2)<20).mean()) for c in targets]
 assert fractions[0]>.4 and fractions[1]>.1 and fractions[2]>.08,fractions
 row=a[105,:,0]>180;transitions=int(np.sum(row[1:]!=row[:-1]));assert transitions>=12
 assert (a[80,:,0]>180).sum()<(a[105,:,0]>180).sum()
 return {'palette_fractions':fractions,'diamond_row_transitions':transitions}
a=np.array(Image.open(R/'maps/sadu-color.png').convert('RGB'));r=pattern(a)
try:pattern(np.full_like(a,143))
except AssertionError:r['flat_map_negative_rejected']=True
else:raise AssertionError('Flat map escaped')
p=np.array(Image.open(R/'poster.png').convert('RGBA'));assert p[:,:,3].max()>200 and (p[:,:,:3].max(axis=2)>25).mean()>.10,'Blank poster'
for f in ['kuwait.blend','kuwait.glb','kuwait-v1.html']:assert (R/f).stat().st_size>1000
assert (R/'kuwait-v1.html').stat().st_size<5_000_000
r['poster_nonblack_fraction']=float((p[:,:,:3].max(axis=2)>25).mean());r['status']='PASS';(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r))
