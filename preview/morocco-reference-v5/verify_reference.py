"""Reference-identity gates, not generic variance or material-name acceptance."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
from glb_tools import load,view,accessor,uv
R=Path(__file__).resolve().parent;O=R.parent/'morocco-saturn-v4'
a=np.asarray(Image.open(R/'maps/reference-color.png'),dtype=float);front=a[:,758:1354]
raw=np.asarray(Image.open(R/'references/front-rectified-observed.png'),dtype=float)
mask=np.asarray(Image.open(R/'references/front-rectified-mask.png'))>0;mask[:20]=True;mask[-20:]=True;mask[:,:25]=True;mask[:,-25:]=True
# Independently reconstruct declared global reflectance calibration on observed pixels.
gain=1+.07*(np.arange(256)/255-.5);expected=raw*gain[:,None,None];weight=np.clip(expected.mean(axis=-1)/190,.25,1)[...,None];expected*=1-weight*np.array([.12,.16,.18]);expected=np.clip(expected,0,255)
err=np.abs(front-expected)[~mask];mae=float(err.mean());assert mae<1.1,mae
# Fine layer location and horizontal variation survive calibrated source sampling.
valid=(~mask[:,1:])&(~mask[:,:-1]);grad=np.diff(front.mean(axis=-1),axis=1);refgrad=np.diff(expected.mean(axis=-1),axis=1)
corr=float(np.corrcoef(grad[valid],refgrad[valid])[0,1]);assert corr>.98,corr
# Broad vertical distribution, not just variance: row-color profile from unoccluded pixels.
rowA=np.array([front[y][~mask[y]].mean(axis=0) for y in range(20,236)]);rowB=np.array([expected[y][~mask[y]].mean(axis=0) for y in range(20,236)])
rowcorr=float(np.corrcoef(rowA.ravel(),rowB.ravel())[0,1]);assert rowcorr>.99
old=np.asarray(Image.open(O/'maps/saturn-color.png').crop((384,0,640,256)).resize((596,256)),dtype=float)
oldmae=float(np.abs(old-expected)[~mask].mean());assert oldmae>mae+20,oldmae
# All map seams truly periodic; physical sampling 160px/unit both axes.
for name in ['color','normal','orm']:
 ar=np.asarray(Image.open(R/f'maps/reference-{name}.png'));assert ar.shape[:2]==(256,2112) and np.array_equal(ar[:,0],ar[:,-1])
assert abs(2112/13.2-256/1.6)<1e-9
# Independent corner limits: close points on adjacent faces share perimeter coordinate.
corner_errors=[]
for x,y in [(-1.86,-1.44),(1.86,-1.44),(-1.86,1.44),(1.86,1.44)]:
 a1=uv(x*(1-1e-7),y,.84);a2=uv(x,y*(1-1e-7),.84);corner_errors.append(float(np.max(np.abs(a1-a2))))
assert max(corner_errors)<1e-6
j,b=load(R/'baseline/morocco.glb');n,nb=load(R/'morocco.glb')
allowed={j['images'][i]['bufferView'] for i in [3,4,5]}
for node in j['nodes']:
 if node.get('name','').startswith('Rose stone'):
  for p in j['meshes'][node['mesh']]['primitives']:allowed.add(j['accessors'][p['attributes']['TEXCOORD_0']]['bufferView'])
for i in range(len(j['bufferViews'])):
 if i not in allowed:assert view(j,b,i)==view(n,nb,i),i
for f in ['viewer.js','viewer.bundle.js','motion.mjs','template.html']:assert (O/f).read_bytes()==(R/f).read_bytes(),f
prev=json.loads((R/'previous-hashes.json').read_text())
for name,h in prev.items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==h,name
assert hashlib.sha256((R/'references/primary-morocco.png').read_bytes()).hexdigest()=='2c29c7e684424ad1f20ca2682e9a1280cdd87db36423b99ba3da22726a12f87f'
r={'unoccluded_source_pixel_mean_absolute_error_255':mae,'horizontal_detail_correlation':corr,'vertical_row_palette_correlation':rowcorr,'rejected_v4_reference_error':oldmae,'observed_front_pixels_tested':int((~mask).sum()),'all_map_periodic_endpoints_exact':True,'physical_texels_per_unit':160,'corner_uv_limit_max_error':max(corner_errors),'all_nonbody_buffer_views_byte_identical':True,'viewer_motion_template_bundle_byte_identical':True,'previous_v4_files_hash_verified':len(prev),'primary_original_hash_verified':True,'visual_limit':'Pixel identity outside masks proves source retention, not intrinsic albedo recovery or whole-render equality. Occluded and hidden material reconstructed; local patch transitions remain.'}
(R/'reference-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
