"""One scoped correction from frozen originals. Does not regenerate landmarks."""
import bpy,json,sys
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];slug=sys.argv[sys.argv.index('--')+1];root=R/'preview'/f'{slug}-repair-v2'
bpy.ops.wm.open_mainfile(filepath=str(root/'historical-v1'/f'{slug}.blend'),use_scripts=False);bpy.context.view_layer.update()
def bounds(o):
 v=[o.matrix_world@v.co for v in o.data.vertices];return [[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]]
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')];before={o.name:bounds(o) for o in meshes};changes=[];pairs=[];negative=[]
if slug=='algeria':
 for name in ['Mineral seam / side','Mineral seam / side.001']:
  o=bpy.data.objects[name];corners=[c for c in meshes if c.name.startswith('Sandstone / rim corner') and c.location.x*o.location.x>0]
  for c in corners:
   a=before[o.name];b=before[c.name];gap=max(b[0][1]-a[1][1],a[0][1]-b[1][1]);assert .024<gap<.026;negative.append({'pair':[name,c.name],'axis_gap':gap});pairs.append([name,c.name])
  for v in o.data.vertices:v.co.y*=2.13/2.05
  changes.append(name)
elif slug=='guyana':
 longs=[bpy.data.objects[n] for n in ['Seam / long','Seam / long.001']];sides=[bpy.data.objects[n] for n in ['Seam / side','Seam / side.001']]
 for o in longs:
  for c in sides:
   a=before[o.name];b=before[c.name];gap=max(max(b[0][i]-a[1][i],a[0][i]-b[1][i],0) for i in range(3));assert gap>.03;negative.append({'pair':[o.name,c.name],'axis_gap':gap});pairs.append([o.name,c.name])
 for o in longs+sides:
  top=max(v.co.z for v in o.data.vertices);bottom=min(v.co.z for v in o.data.vertices)
  for v in o.data.vertices:
   if o in longs:v.co.x*=3.40/3.28
   else:v.co.y*=2.30/2.05
   # Seat all strips into shell; preserve long-strip tops, side tops 4mm lower
   # to avoid coplanar overlapping top faces at the four junctions.
   v.co.z=top+(v.co.z-top)*(1+(.024 if o in longs else .020)/(top-bottom))-(0 if o in longs else .004)
  changes.append(o.name)
  support=('Body / sandstone long' if o in longs else 'Body / sandstone side')+('.001' if o.name.endswith('.001') else '')
  pairs.append([o.name,support])
else:raise ValueError(slug)
bpy.context.view_layer.update()
for a,b in pairs:assert tree(bpy.data.objects[a]).overlap(tree(bpy.data.objects[b])),('missing surface contact',a,b)
after={o.name:bounds(o) for o in meshes};assert all(before[n]==after[n] for n in before if n not in changes)
evidence={'correction_passes':1,'changed_objects':changes,'baseline_disconnected_pairs':negative,'repaired_surface_intersections':pairs,'before':{n:before[n] for n in changes},'after':{n:after[n] for n in changes},'untargeted_bounds_exact':True}
(root/'repair-check.json').write_text(json.dumps(evidence,indent=2))
s=bpy.context.scene;s.render.threads_mode='FIXED';s.render.threads=4;s.cycles.use_denoising=False;s.render.use_compositing=False
bpy.ops.wm.save_as_mainfile(filepath=str(root/f'{slug}.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Lid_Hinge'];bpy.ops.export_scene.gltf(filepath=str(root/f'{slug}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
s.render.filepath=str(root/'poster.png');bpy.ops.render.render(write_still=True)
print(json.dumps(evidence,indent=2))
