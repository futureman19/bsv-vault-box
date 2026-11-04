import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'southern-ocean.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
parts=[o for o in bpy.data.objects if o.name.startswith(('Pack floe','Tabular iceberg'))]
def validate(parts):
 assert len(parts)==10
 for o in parts:
  assert o.parent==lid,('detached',o.name)
  vs=[o.matrix_world@v.co for v in o.data.vertices];zs=[v.z for v in vs]
  assert abs(min(zs)-1.974)<1e-5
  top=[v.z for v in vs if v.z>min(zs)+.02];assert max(top)-min(top)<1e-5
  assert all(abs(v.x)<1.6 and abs(v.y)<.96 for v in vs)
 berg=bpy.data.objects['Tabular iceberg'];vs=[berg.matrix_world@v.co for v in berg.data.vertices]
 assert .35<max(v.z for v in vs)-min(v.z for v in vs)<.55
 # Disjoint XY bounds are conservative proof of blue space between prisms.
 bounds=[]
 for o in parts:
  v=[o.matrix_world@p.co for p in o.data.vertices];bounds.append((o.name,min(p.x for p in v),max(p.x for p in v),min(p.y for p in v),max(p.y for p in v)))
 for i,a in enumerate(bounds):
  for b in bounds[i+1:]:assert a[2]<b[1] or b[2]<a[1] or a[4]<b[3] or b[4]<a[3],('overlapping XY',a[0],b[0])
 return bounds
bounds=validate(parts)
o=parts[0];o.parent=None
try:validate(parts)
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative detached-ornament control not rejected')
o.parent=lid
# Compare baseline pivot matrices via independently reopened scenes.
current={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,rows in current.items():assert max(abs(rows[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
result={'status':'PASS','floe_count':9,'tabular_berg_count':1,'level_plateaus':True,'rooted_on_lid':True,'separated_xy_bounds':bounds,'baseline_pivots_identical':True,'detached_negative_control_rejected':negative}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME PASS',json.dumps(result))
