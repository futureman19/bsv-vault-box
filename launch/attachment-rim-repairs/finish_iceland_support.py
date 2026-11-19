import bpy,json
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];root=R/'launch/attachment-rim-repairs/finish/iceland/verified'
bpy.ops.wm.open_mainfile(filepath=str(root/'iceland.blend'),use_scripts=False);bpy.context.view_layer.update()
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
names=['Basalt fracture / rear.008','Basalt fracture / right.011','Basalt fracture / right.005','Basalt fracture / right.007','Basalt fracture / right.003','Basalt fracture / front.021'];walls=[o for o in bpy.data.objects if o.name.startswith('Interior wall')];out=[]
for name in names:
 o=bpy.data.objects[name];hits=[w.name for w in walls if tree(o).overlap(tree(w))];assert hits,(name,'unsupported');out.append({'mesh':name,'intersects_interior_walls':hits})
(root/'rim-support-check.json').write_text(json.dumps({'pixel_identification':'rim-pixel-identification.json','identified_projections':out,'verdict':'Identified thin projections belong to supported basalt/continuous interior walls, not detached trim. No geometry repair warranted.','limitations':'Sampled image-pixel ownership and BVH surface contacts, not manufacturing certification.'},indent=2));print(out)
