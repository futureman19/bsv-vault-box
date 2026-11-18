import bpy,json,hashlib,struct
from pathlib import Path
R=Path(__file__).resolve().parent

def source(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update();out={}
 for o in bpy.data.objects:
  if o.name.startswith('Studio') or o.type not in ['MESH','EMPTY']:continue
  out[o.name]=dict(matrix=[list(row) for row in o.matrix_world],parent=o.parent.name if o.parent else None)
  if o.type=='MESH':out[o.name].update(vertices=[list(v.co) for v in o.data.vertices],polygons=[list(p.vertices) for p in o.data.polygons],uv=[[list(u.uv) for u in layer.data] for layer in o.data.uv_layers])
 return out
old=source(R/'baseline-v7.blend');new=source(R/'united-states.blend');assert old==new
images=[]
for im in bpy.data.images:
 if im.packed_file:
  assert im.packed_file.data==(R/'maps'/im.name).read_bytes();images.append(im.name)
assert len(images)==3
heights={}
for name,path in [('v8',R/'baseline-v8.glb'),('v9',R/'united-states.glb')]:
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path));bpy.context.view_layer.update()
 o=bpy.data.objects['Lid / polished slab'];z=[(o.matrix_world@v.co).z for v in o.data.vertices];heights[name]=dict(min=min(z),max=max(z),thickness=max(z)-min(z))
assert abs(heights['v8']['thickness']-.06)<1e-5 and abs(heights['v9']['thickness']-.30)<1e-5
out=dict(PASS=True,v7_v9_exact_source_meshes_uvs_pivots=True,objects=len(new),source_packed_bytes_equal_maps=images,actual_export_lids=heights)
(R/'restoration-check.json').write_text(json.dumps(out,indent=2));print(out)
