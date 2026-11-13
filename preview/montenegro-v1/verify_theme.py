import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.view_layer.update()
expected={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'montenegro.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
for n,m in expected.items():assert max(abs(v-m[i][j]) for i,row in enumerate(bpy.data.objects[n].matrix_world) for j,v in enumerate(row))<1e-7
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Karst /','Forest /','Tara /'))]
def ownership():
 assert ornaments and all(o.parent==lid for o in ornaments)
ownership();ornaments[0].parent=None
try:ownership()
except AssertionError:negative=True
else:raise AssertionError('Detached ornament not rejected')
ornaments[0].parent=lid;bpy.context.view_layer.update()
# Reload so the deliberate control cannot affect subsequent geometric proof.
bpy.ops.wm.open_mainfile(filepath=str(R/'montenegro.blend'),use_scripts=False);bpy.context.view_layer.update()
dep=bpy.context.evaluated_depsgraph_get();hits=[]
for i in range(61):
 x=-1.45+2.9*i/60;y=.12*math.sin(2.2*x)
 hit,loc,n,ix,obj,mat=bpy.context.scene.ray_cast(dep,Vector((x,y,4)),Vector((0,0,-1)))
 assert hit and obj.name=='Tara / continuous river',(x,obj.name if obj else None)
 hits.append([x,y,loc.z])
assert len([o for o in bpy.data.objects if o.name.startswith('Karst /')])==2
assert not any('Cedar' in o.name or 'Granite' in o.name for o in bpy.data.objects)
# Water topological connectedness, all polygon vertices reachable.
o=bpy.data.objects['Tara / continuous river'];edges={v.index:set() for v in o.data.vertices}
for e in o.data.edges:a,b=e.vertices;edges[a].add(b);edges[b].add(a)
seen={0};todo=[0]
while todo:
 for n in edges[todo.pop()]-seen:seen.add(n);todo.append(n)
assert len(seen)==len(edges)
assert all(o.parent==bpy.data.objects['Lid_Hinge'] for o in bpy.data.objects if o.name.startswith(('Karst /','Forest /','Tara /')))
result={'status':'PASS','pivot_matrix_match':True,'detached_ornament_negative_control_rejected':negative,'ornament_meshes':len(ornaments),'river_connected_vertices':len(seen),'exposed_centerline_rays':hits,'geographic_accuracy_claimed':False}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('PASS theme, pivots, river continuity and 61 exposed rays')
