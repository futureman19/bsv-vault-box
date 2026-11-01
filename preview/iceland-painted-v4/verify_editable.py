"""Reopen candidate; compare actual triangle world positions to approved source.
Also prove saved source UVs/images are those carried by delivered GLB.
"""
import bpy,json,struct,hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent

def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update();out={}
 for o in bpy.data.objects:
  if o.type!='MESH' or o.name.startswith('Studio'):continue
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles();a=[]
  for tri in m.loop_triangles:
   a.extend(tuple(round(float(v),5) for v in o.matrix_world@m.vertices[i].co) for i in tri.vertices)
  out[o.name]=Counter(a);ev.to_mesh_clear()
 return out
original=snapshot(R.parent/'iceland-lightweight-v3/original/iceland.blend');candidate=snapshot(R/'iceland.blend')
assert original.keys()==candidate.keys()
# Float export/import can cross a decimal rounding boundary on two latch barrels.
# Compare unmatched rounded corners within 0.00002 units, retaining multiplicity.
import math
max_delta=0
for name in original:
 missing=original[name]-candidate[name];extra=candidate[name]-original[name]
 for point,count in missing.items():
  nearest=min((q for q,c in extra.items() if c>=count),key=lambda q:math.dist(point,q));delta=math.dist(point,nearest)
  assert delta<=.00002,(name,delta);max_delta=max(max_delta,delta);extra[nearest]-=count
 assert sum(extra.values())==0
b=(R/'iceland.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);blob=b[28+n:]
images=[]
for im in bpy.data.images:
 if im.packed_file and im.name.startswith('paint-'):
  disk=(R/'textures'/im.name).read_bytes();assert bytes(im.packed_file.data)==disk;images.append(im.name)
assert len(images)==3
# UV corner comparison keyed by local vertex position, independent of importer merging.
for node in g['nodes']:
 if 'mesh' not in node:continue
 gm=g['meshes'][node['mesh']]
 if not any(p['material']<=5 for p in gm['primitives']):continue
 o=bpy.data.objects[node['name']];m=o.data;m.calc_loop_triangles();actual=[];expected=[]
 for tr in m.loop_triangles:
  for li in tr.loops:
   co=m.vertices[m.loops[li].vertex_index].co;uv=m.uv_layers.active.data[li].uv
   actual.append(tuple(round(v,5) for v in (co.x,co.z,-co.y,uv.x,1-uv.y)))
 def array(ai,components,fmt):
  a=g['accessors'][ai];bv=g['bufferViews'][a['bufferView']];sz=struct.calcsize(fmt)*components
  return [struct.unpack_from('<'+fmt*components,blob,bv.get('byteOffset',0)+a.get('byteOffset',0)+i*bv.get('byteStride',sz)) for i in range(a['count'])]
 for p in gm['primitives']:
  pos=array(p['attributes']['POSITION'],3,'f');uv=array(p['attributes']['TEXCOORD_0'],2,'f');it=g['accessors'][p['indices']]['componentType'];ids=array(p['indices'],1,{5123:'H',5125:'I',5121:'B'}[it])
  for (i,) in ids:expected.append(tuple(round(v,5) for v in (*pos[i],*uv[i])))
 assert Counter(actual)==Counter(expected),node['name']
result={'source_reopened':True,'world_triangle_corners_tolerance':.00002,'max_rounded_corner_delta':max_delta,'meshes':len(candidate),'source_uv_triangle_corners_match_glb':True,'packed_image_bytes_match':images,'editable_source':'Original evaluated geometry imported from portable GLB; original procedural source preserved separately'}
(R/'editable-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
