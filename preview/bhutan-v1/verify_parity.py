import bpy,json
from pathlib import Path
from mathutils.kdtree import KDTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'bhutan.blend'),use_scripts=False)
def vertices():
 out=[];dep=bpy.context.evaluated_depsgraph_get()
 for o in bpy.data.objects:
  if o.type!='MESH' or o.name.startswith('Studio'):continue
  ev=o.evaluated_get(dep);m=ev.to_mesh();out.extend([o.matrix_world@v.co for v in m.vertices]);ev.to_mesh_clear()
 return out
source=vertices();image_names=[i.name for i in bpy.data.images if i.packed_file];assert len(image_names)>=3
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(R/'bhutan.glb'));bpy.context.view_layer.update();export=vertices()
def distance(a,b):
 kd=KDTree(len(b))
 for i,v in enumerate(b):kd.insert(v,i)
 kd.balance();return max(kd.find(v)[2] for v in a)
ab=distance(source,export);ba=distance(export,source);assert max(ab,ba)<1e-5,(ab,ba)
r=dict(source_vertices=len(source),imported_vertices=len(export),source_to_glb_max=ab,glb_to_source_max=ba,source_packed_images=image_names,source_and_export_geometry_match=True)
(R/'parity-check.json').write_text(json.dumps(r,indent=2));print(r)
