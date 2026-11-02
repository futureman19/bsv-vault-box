from pathlib import Path
import json,hashlib,io
import numpy as np
from PIL import Image
from glb_tools import load,accessor,view
R=Path(__file__).resolve().parent;old=R.parent/'morocco-reference-v5'
a,ab=load(R/'baseline/morocco.glb');b,bb=load(R/'morocco.glb');out={}
assert a['nodes']==b['nodes'] and a['scenes']==b['scenes'];out['all_nodes_parents_transforms_exact']=True
for i,m in enumerate(a['materials']):
 if i==7:
  expected=json.loads(json.dumps(m));expected['pbrMetallicRoughness']['baseColorFactor']=[.9,.9,.9,1];assert b['materials'][i]==expected
 else:assert m==b['materials'][i]
for i,im in enumerate(a['images']):assert view(a,ab,im['bufferView'])==view(b,bb,b['images'][i]['bufferView'])
out['all_original_image_payloads_exact']=True;out['old_materials_exact_except_body_factor']=True
changed={'Lid / polished slab','Tile bed / long','Tile bed / long.001','Tile bed / return','Tile bed / return.001'};ceramic=[];same=[]
def tris(j,bin,mesh):
 ts=[]
 for p in mesh['primitives']:
  pos=accessor(j,bin,p['attributes']['POSITION']);idx=accessor(j,bin,p['indices']).ravel();ts.extend(pos[idx].reshape(-1,3,3))
 return sorted(tuple(sorted(tuple(x) for x in np.round(t,6))) for t in ts)
for n in a['nodes']:
 if 'mesh' not in n:continue
 m1=a['meshes'][n['mesh']];m2=b['meshes'][n['mesh']]
 if n['name'].startswith('Ceramic tessera'):ceramic.append(n['name']);continue
 assert tris(a,ab,m1)==tris(b,bb,m2),n['name'];same.append(n['name'])
 if n['name'] not in changed:
  for p,q in zip(m1['primitives'],m2['primitives']):
   assert p['material']==q['material'];assert p['attributes'].keys()==q['attributes'].keys()
   for k in p['attributes']:assert np.array_equal(accessor(a,ab,p['attributes'][k]),accessor(b,bb,q['attributes'][k])),(n['name'],k)
out.update(unchanged_geometry_meshes=len(same),changed_geometry_only=ceramic,body_UV_registration_and_all_non_target_attributes_exact=True)
for f in ['viewer.js','viewer.bundle.js','motion.mjs','template.html']:assert (old/f).read_bytes()==(R/f).read_bytes(),f
out['viewer_controls_lighting_camera_motion_bytes_exact']=True
# Bounds on actual RGB darkening, including gamma encoding. No texture noise added.
body=np.asarray(Image.open(io.BytesIO(view(a,ab,a['images'][4]['bufferView']))),dtype=float)[:,:,:3]/255
lin=np.where(body<=.04045,body/12.92,((body+.055)/1.055)**2.4);dark=lin*.9;srgb=np.where(dark<=.0031308,dark*12.92,1.055*dark**(1/2.4)-.055)
ratio=srgb/(body+1e-12);valid=body>.08
assert ratio[valid].min()>.92 and ratio[valid].max()<.96
out['body_tone']={'linear_multiplier':.9,'rgb_ratio_min':float(ratio[valid].min()),'rgb_ratio_max':float(ratio[valid].max()),'new_black_clipping_pixels':int(((srgb==0)&(body>0)).sum()),'no_recolor':True,'no_new_noise':True}
# Decode production images from the final GLB, not source filenames.
def decode(material):
 m=next(m for m in b['materials'] if m['name']==material);t=b['textures'][m['pbrMetallicRoughness']['baseColorTexture']['index']];im=b['images'][t['source']];return np.asarray(Image.open(io.BytesIO(view(b,bb,im['bufferView']))).convert('RGB'))
w=decode('Cedar / warm reference-grained vertical edges');lum=w.mean(2);dx=float(np.abs(np.diff(lum,axis=1)).mean());dy=float(np.abs(np.diff(lum,axis=0)).mean())
# Grain direction is assessed at a 3px line scale, not single-pixel photographic pores.
from PIL import ImageFilter
smooth=np.asarray(Image.fromarray(w).filter(ImageFilter.GaussianBlur(3)),dtype=float).mean(2)
gx=float(np.abs(np.diff(smooth,axis=1)).mean());gy=float(np.abs(np.diff(smooth,axis=0)).mean())
assert w.shape==(128,1024,3) and lum.std()>5 and gy>gx*1.5
# Nonuniform horizontal-detail image, not constant painted stripes.
assert float(lum.std(axis=1).mean())>3
out['portable_edge_grain']={'shape':list(w.shape),'mean_rgb':w.mean((0,1)).tolist(),'std':float(lum.std()),'horizontal_derivative':dx,'vertical_derivative':dy,'within_row_variation':float(lum.std(axis=1).mean()),'actual_embedded_image':True}
t=decode('Ceramic / reference emerald ivory rosette');expected=np.asarray(Image.open(R/'maps/ceramic-atlas.png').convert('RGB'));assert np.array_equal(t,expected)
colors,counts=np.unique(t.reshape(-1,3),axis=0,return_counts=True);assert len(colors)==3
source=np.asarray(Image.open(R/'references/tile-source-swatch.png'),dtype=float);green=(source[:,:,1]-source[:,:,0]>2)&(source[:,:,1]>source[:,:,2]*1.07);cream=(source.mean(2)>105)&~green;labels=np.where(cream,2,np.where(green,1,0));palette=np.array([[24,28,22],[22,98,68],[220,211,179]],dtype=np.uint8)
assert np.array_equal(np.asarray(Image.open(R/'maps/tile-repeat.png')),palette[labels])
out['reference_correspondence']={'decoded_atlas_source_exact':True,'observed_motif_label_agreement':1.0,'pigments':colors.tolist(),'pigment_pixel_counts':counts.tolist(),'not_visual_equivalence':'Single source motif repeated and mitered; rendered match remains partial.'}
assert (R/'morocco-finish-v6.html').stat().st_size<5_000_000
# Immutable prior version read-back.
ledger=json.loads((R/'previous-hashes.json').read_text())
for f,h in ledger.items():assert hashlib.sha256((old/f).read_bytes()).hexdigest()==h,f
out['previous_version_immutable_files']=len(ledger)
(R/'finish-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
