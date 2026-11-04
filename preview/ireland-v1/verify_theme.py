import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'ireland.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
clints=[o for o in bpy.data.objects if o.name.startswith('Pavement / clint')]
def validate():
 assert len(clints)==20
 for o in clints:
  assert o.parent==lid,('not lid owned',o.name)
  pts=[o.matrix_world@v.co for v in o.data.vertices]
  assert max(abs(v.x) for v in pts)<1.55 and max(abs(v.y) for v in pts)<.85
  assert 2.07<max(v.z for v in pts)<2.24
  assert min(v.z for v in pts)<1.98
validate()
# Deliberately detach a real ornament in memory: oracle must reject it.
o=clints[0];o.parent=None
try:validate()
except AssertionError as e:negative=str(e)
else:raise AssertionError('detached ornament accepted')
# Reload restores exact saved source without writing mutation.
bpy.ops.wm.open_mainfile(filepath=str(R/'ireland.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];clints=[o for o in bpy.data.objects if o.name.startswith('Pavement / clint')];validate()
def ray(x,y):
 hit,loc,n,i,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit
 return obj.name,float(loc.z)
centers=[]
for row in range(4):
 for col in range(5):
  name,z=ray(-1.24+col*.62,-.6375+row*.425);assert name.startswith('Pavement / clint');centers.append([name,z])
gaps=[]
for row in range(4):
 for col in range(4):
  name,z=ray(-.93+col*.62,-.6375+row*.425);assert name=='Pavement / grike bed';gaps.append([name,z])
# Independently compare inherited pivots after evaluation in both saved scenes.
pivots={n:[list(r) for r in bpy.data.objects[n].matrix_local] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_local[i][j]) for i in range(4) for j in range(4))<1e-6
result={'status':'PASS','clints':20,'center_rays':centers,'grike_rays':gaps,'detached_ornament_negative_control':negative,'original_pivots_preserved':True,'relief_bounds_pass':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
