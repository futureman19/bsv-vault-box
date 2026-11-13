"""Independent saved-source theme gates; negative control is detached real ridge."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'new-zealand.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
def check():
 objs=[bpy.data.objects[n] for n in ['Ridge / west','Ridge / east','Fiord / continuous water']]
 assert all(o.parent==lid for o in objs),'Terrain must travel with lid'
 heights=[]
 for o in objs[:2]:
  vs=[o.matrix_world@v.co for v in o.data.vertices];z=[v.z for v in vs]
  assert min(z)<=1.978 and 2.45<max(z)<2.80,(o.name,min(z),max(z))
  heights.append([o.name,min(z),max(z)])
 hits=[]
 for i in range(17):
  y=-.82+1.64*i/16;x=.16*math.sin(3*y)
  hit,loc,normal,index,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3.5)),Vector((0,0,-1)))
  assert hit and obj.name=='Fiord / continuous water',(i,obj.name if obj else None)
  hits.append([x,y,loc.z])
 water=objs[2];adj={v.index:set() for v in water.data.vertices}
 for edge in water.data.edges:
  a,b=edge.vertices;adj[a].add(b);adj[b].add(a)
 seen={0};todo=[0]
 while todo:
  for k in adj[todo.pop()]-seen:seen.add(k);todo.append(k)
 assert len(seen)==len(adj),'Disconnected water'
 return {'ridge_bounds':heights,'exposed_water_rays':hits,'connected_water_vertices':len(seen),'lid_ancestry':True}
result=check();o=bpy.data.objects['Ridge / west'];o.parent=None
try:check()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Detached ridge negative control was not rejected')
result.update(status='PASS',negative_control={'detached_ridge_rejected':True,'failure':negative})
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME PASS',json.dumps(result))
