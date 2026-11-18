"""One bounded geometry correction, from immutable saved source, not a regeneration."""
import bpy,json,sys
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2]
slug=sys.argv[sys.argv.index('--')+1];root=R/'preview'/f'{slug}-repair-v2'
bpy.ops.wm.open_mainfile(filepath=str(root/'historical-v1'/f'{slug}.blend'),use_scripts=False)
bpy.context.view_layer.update()
def bounds(o):
 v=[o.matrix_world@v.co for v in o.data.vertices];return [[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]]
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')]
before={o.name:bounds(o) for o in meshes};changes=[]
if slug=='ghana':
 o=bpy.data.objects['Dark seam / long'];assert o.location.y<0
 a=before[o.name];gaps={}
 for other in meshes:
  if other==o:continue
  b=before[other.name];gaps[other.name]=max(max(b[0][i]-a[1][i],a[0][i]-b[1][i],0) for i in range(3))
 assert min(gaps.values())>.009,'Baseline must demonstrate separation'
 # Keep upper surface and all horizontal coordinates. Stretch only downward.
 top=max(v.co.z for v in o.data.vertices)
 for v in o.data.vertices:v.co.z=top+(v.co.z-top)*1.5
 changes=[o.name]
 bpy.context.view_layer.update()
 assert tree(o).overlap(tree(bpy.data.objects['Cocoa / long wall'])),'Front trim must intersect supporting shell'
 evidence={'baseline_minimum_axis_gap':min(gaps.values()),'baseline_gaps':gaps,'repaired_front_wall_surface_intersection':True}
else:
 evidence={'baseline_side_corner_gaps':[],'repaired_side_corner_intersections':[]}
 for name in ['Mineral seam / side','Mineral seam / side.001']:
  o=bpy.data.objects[name];corners=[c for c in meshes if c.name.startswith('Mineral rim / corner') and c.location.x*o.location.x>0]
  for c in corners:
   a=before[o.name];b=before[c.name];gap=max(b[0][1]-a[1][1],a[0][1]-b[1][1]);assert .024<gap<.026;evidence['baseline_side_corner_gaps'].append(gap)
  for v in o.data.vertices:v.co.y*=2.13/2.05
  bpy.context.view_layer.update()
  for c in corners:
   assert tree(o).overlap(tree(c)),(o.name,c.name);evidence['repaired_side_corner_intersections'].append([o.name,c.name])
  changes.append(name)
after={o.name:bounds(o) for o in meshes}
assert all(before[n]==after[n] for n in before if n not in changes)
evidence.update(changed_objects=changes,before={n:before[n] for n in changes},after={n:after[n] for n in changes},untargeted_bounds_exact=True,correction_passes=1)
(root/'repair-check.json').write_text(json.dumps(evidence,indent=2))
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.cycles.use_denoising=False
bpy.ops.wm.save_as_mainfile(filepath=str(root/f'{slug}.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Lid_Hinge']
bpy.ops.export_scene.gltf(filepath=str(root/f'{slug}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(root/'poster.png');bpy.ops.render.render(write_still=True)
print(json.dumps(evidence,indent=2))
