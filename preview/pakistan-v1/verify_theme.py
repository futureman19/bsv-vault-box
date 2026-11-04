import bpy,json,sys,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'pakistan.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
ros=[o for o in bpy.data.objects if o.name.startswith('Rosette /')]
def check():
 assert len(ros)==27
 assert all(o.parent==lid for o in ros),'rosette detached from lid'
 bounds=[]
 for o in ros:
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();v=[o.matrix_world@x.co for x in m.vertices];bounds.extend(v);ev.to_mesh_clear()
 assert max(v.z for v in bounds)<2.15
 assert min(v.z for v in bounds)<1.989 and min(v.z for v in bounds)>1.97
 assert all(any(abs(o.matrix_world.translation.x-x)<.001 for o in ros if 'centre' in o.name) for x in [-1.05,0,1.05])
 return {'rosettes':3,'petals':24,'all_lid_parented':True,'relief_z':[min(v.z for v in bounds),max(v.z for v in bounds)]}
result=check();ros[0].parent=None
try:check()
except AssertionError as e:result['negative_control']={'detached_petal_rejected':True,'error':str(e)}
else:raise AssertionError('Negative control incorrectly accepted')
ros[0].parent=lid
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,m in pivots.items():
 assert max(abs(m[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
result['original_pivots_exact']=True;result['status']='PASS'
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
