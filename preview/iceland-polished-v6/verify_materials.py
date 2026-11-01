import bpy,json,struct,math,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'iceland.blend'),use_scripts=False)
b=(R/'iceland.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);checked=[]
for m in g['materials']:
 src=bpy.data.materials[m['name']];p=src.node_tree.nodes.get('Principled BSDF');q=m.get('pbrMetallicRoughness',{})
 if 'baseColorTexture' not in q:assert max(abs(a-c) for a,c in zip(p.inputs['Base Color'].default_value,q.get('baseColorFactor',[1]*4)))<1e-6
 if 'metallicRoughnessTexture' not in q:
  assert abs(p.inputs['Roughness'].default_value-q.get('roughnessFactor',1))<1e-6
  assert abs(p.inputs['Metallic'].default_value-q.get('metallicFactor',1))<1e-6
 t=m.get('extensions',{}).get('KHR_materials_transmission',{}).get('transmissionFactor',0)
 assert abs(p.inputs['Transmission Weight'].default_value-t)<1e-6
 checked.append(m['name'])
bad=[];count=0
for o in bpy.data.objects:
 if o.type!='MESH' or o.name.startswith('Studio'):continue
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
 for v in me.vertices:
  count+=1
  if not all(math.isfinite(x) for x in v.normal) or abs(v.normal.length-1)>.001:bad.append(o.name)
 ev.to_mesh_clear()
assert not bad,bad
images={i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest() for i in bpy.data.images if i.packed_file}
r={'source_materials_match_export_factors':checked,'source_unit_finite_normals':count,'packed_source_image_hashes':images,'provenance':'Authored procedural geometry and compact generated stone maps, not photographic scans'}
(R/'material-provenance.json').write_text(json.dumps(r,indent=2));print(r)
