from pathlib import Path
import json,struct,copy,hashlib
R=Path(__file__).resolve().parent;V=R/'original'
def parse(p):
 b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];return json.loads(b[20:20+n]),b[28+n:]
a,ab=parse(V/'iceland.glb');b,bb=parse(R/'iceland.glb')
assert bb[:len(ab)]==ab
for key in ['nodes','scenes','scene','animations']:
 assert a.get(key)==b.get(key),key
bm=copy.deepcopy(b['meshes'])
for mesh in bm:
 for p in mesh['primitives']:p['attributes'].pop('TEXCOORD_0',None) if a['materials'][p['material']]['name'].startswith('Basalt /') else None
assert a['meshes']==bm
assert a['accessors']==b['accessors'][:len(a['accessors'])]
for i,m in enumerate(a['materials']):
 if not m['name'].startswith('Basalt /'):assert m==b['materials'][i]
for name in ['viewer.js','viewer.bundle.js','motion.mjs']:
 assert (R/name).read_bytes()==(V/name).read_bytes(),name
result={'original_binary_prefix_identical':True,'nodes_transforms_pivots_identical':True,'geometry_accessors_indices_normals_identical':True,'all_nonbasalt_materials_identical':True,'entire_viewer_and_motion_byte_identical':True,'original_glb_sha256':hashlib.sha256((V/'iceland.glb').read_bytes()).hexdigest()}
(R/'preservation-check.json').write_text(json.dumps(result,indent=2));print(result)
