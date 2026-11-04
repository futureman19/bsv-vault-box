import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'united-states.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-8
lid=bpy.data.objects['Lid_Hinge'];river=bpy.data.objects['River / continuous winding channel'];rims=[o for o in bpy.data.objects if o.name.startswith('Canyon rim /')]
def ancestry():assert river.parent==lid and all(o.parent==lid for o in rims)
ancestry();river.parent=None
try:ancestry();raise RuntimeError('negative control failed to reject')
except AssertionError:negative=True
river.parent=lid
assert len(rims)==6
levels={s:sorted(set(round(max((o.matrix_world@v.co).z for v in o.data.vertices),3) for o in rims if o.name.startswith('Canyon rim / '+s+' '))) for s in ['-1','1']}
assert all(len(v)==3 and .18<=max(v)-1.978<=.65 for v in levels.values())
# Edge graph connectivity of actual water mesh.
adj={i:set() for i in range(len(river.data.vertices))}
for e in river.data.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen=set();todo=[0]
while todo:
 i=todo.pop()
 if i not in seen:seen.add(i);todo.extend(adj[i]-seen)
assert len(seen)==len(adj)
coords=[river.matrix_world@v.co for v in river.data.vertices];assert max(v.x for v in coords)-min(v.x for v in coords)>=2.2
bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();down=[];camera=[]
for i in range(41):
 x=-1.4+i*2.8/40;y=.15*math.sin(x*2.7)+.04*math.sin(x*5)
 hit,loc,_,_,obj,_=bpy.context.scene.ray_cast(dep,Vector((x,y,3)),Vector((0,0,-1)))
 down.append(hit and obj==river)
 origin=bpy.context.scene.camera.location;target=Vector((x,y,2.005));direction=(target-origin).normalized()
 hit,loc,_,_,obj,_=bpy.context.scene.ray_cast(dep,origin,direction);camera.append(hit and obj==river)
assert all(down);assert sum(camera)>=20,('River hidden from source hero',sum(camera))
r={'PASS':True,'same_pivots':True,'rim_levels':levels,'river_connected_vertices':len(seen),'river_downward_rays':sum(down),'river_hero_visible_rays':sum(camera),'sample_count':41,'detached_river_negative_rejected':negative}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',r)
