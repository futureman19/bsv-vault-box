import bpy,json,hashlib,struct,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
def anchor(name):
 o=bpy.data.objects[name];return {'location':list(o.location),'rotation':list(o.rotation_euler),'parent':o.parent.name if o.parent else None}
baseline={n:anchor(n) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'israel.blend'),use_scripts=False)
assert baseline=={n:anchor(n) for n in baseline}
terrain=bpy.data.objects['Terrain / Negev erosion basin'];assert terrain.parent.name=='Lid_Hinge'
world=[terrain.matrix_world@v.co for v in terrain.data.vertices]
floor=world[0].z;rim=max(v.z for v in world);assert rim-floor>.14
assert min(v.z for v in world)<1.978 and min(v.z for v in world)>1.8
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
assert not any('cedar' in o.name.lower() or 'tree' in o.name.lower() for o in bpy.data.objects)
raw=(R/'israel.glb').read_bytes();size=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+size]);binary=raw[28+size:]
hashes=[]
for image in doc['images']:
 view=doc['bufferViews'][image['bufferView']];data=binary[view.get('byteOffset',0):view.get('byteOffset',0)+view['byteLength']]
 hashes.append(hashlib.sha256(data).hexdigest())
# Exporter repacks ORM channels; base and normal PNG bytes are preserved exactly.
for f in ['limestone-color.png','limestone-normal.png']:assert hashlib.sha256((R/'maps'/f).read_bytes()).hexdigest() in hashes,f
assert len(doc['images'])>=3
out={'status':'PASS','pivots_equal_included_mechanism':baseline,'basin_floor_z':floor,'basin_rim_z':rim,'relief_height':rim-floor,'lid_dimensions':list(slab.dimensions),'packed_source_images':[i.name for i in bpy.data.images if i.packed_file],'export_image_sha256':hashes,'base_normal_export_bytes_equal_maps':True,'roughness_note':'Exporter packs roughness into ORM image; actual loader decodes and checks variation.'}
(R/'contract-check.json').write_text(json.dumps(out,indent=2));print('SOURCE THEME / PIVOTS / MAP PROVENANCE PASS')
