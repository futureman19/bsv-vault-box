import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
names=['Lid_Hinge','Latch_Pivot'];base={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in names}
bpy.ops.wm.open_mainfile(filepath=str(R/'slovenia.blend'),use_scripts=False);bpy.context.view_layer.update()
for n in names:assert max(abs(a-b) for row,r in zip(base[n],bpy.data.objects[n].matrix_world) for a,b in zip(row,r))<1e-7
lid=bpy.data.objects['Lid_Hinge'];land=[o for o in bpy.data.objects if o.name.startswith('Landscape')]
def attached():return all(o.parent==lid for o in land)
assert attached() and len(land)==21
river=bpy.data.objects['Landscape / Soca continuous inlay'];river.parent=None
assert not attached();river.parent=lid
# Restore exact saved pose after deliberately rejected detached control.
bpy.ops.wm.open_mainfile(filepath=str(R/'slovenia.blend'),use_scripts=False);bpy.context.view_layer.update()
river=bpy.data.objects['Landscape / Soca continuous inlay'];dep=bpy.context.evaluated_depsgraph_get();samples=[]
for i in range(47):
 x=-1.4+(i+1)*2.8/48;y=-.15+.18*math.sin(x*2.8)
 hit,loc,n,idx,o,m=bpy.context.scene.ray_cast(dep,Vector((x,y,3.5)),Vector((0,0,-1)))
 assert hit and o==river,(i,o.name if o else None)
 samples.append(list(loc))
# Continuous river mesh connectivity, not only matching names.
adj={i:set() for i in range(len(river.data.vertices))}
for e in river.data.edges:
 a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen={0};todo=[0]
while todo:
 for b in adj[todo.pop()]-seen:seen.add(b);todo.append(b)
assert len(seen)==len(adj)
for o in bpy.data.objects:
 if o.name.startswith('Landscape'):assert max((o.matrix_world@v.co).z for v in o.data.vertices)<2.85
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
r={'status':'PASS','pivot_matrices_preserved':base,'landscape_meshes':21,'detached_ornament_negative_control':'REJECTED as expected','river_connected_vertices':len(seen),'unoccluded_vertical_channel_samples':samples,'slab_dimensions':list(slab.dimensions),'landscape_max_z_limit':2.85}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS')
