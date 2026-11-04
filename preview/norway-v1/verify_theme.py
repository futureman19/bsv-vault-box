"""Independent saved-source design gates and deliberate detached-water negative."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'norway.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];water=bpy.data.objects['Fjord / continuous water']
def ancestry():
 for o in bpy.data.objects:
  if o.name.startswith(('Fjord bank','Fjord /')):assert o.parent==lid,('Detached terrain',o.name)
ancestry();water.parent=None
try:ancestry();raise RuntimeError('Negative control failed to reject')
except AssertionError as e:negative=str(e)
water.parent=lid;bpy.context.view_layer.update();ancestry()
banks=[o for o in bpy.data.objects if o.name.startswith('Fjord bank')];assert len(banks)==2
peaks=[max((o.matrix_world@v.co).z for v in o.data.vertices) for o in banks];assert all(2.85<z<3.20 for z in peaks),peaks
assert all(min((o.matrix_world@v.co).z for v in o.data.vertices)<1.978 for o in banks)
fall=bpy.data.objects['Fjord / pale waterfall'];zs=[(fall.matrix_world@v.co).z for v in fall.data.vertices]
assert min(zs)<2.013 and max(zs)>2.4
rays=[]
for j in range(17):
 y=-.8+j*.1;x=.16*math.sin(y*3.8)+.035*math.cos(y*8)
 hit,loc,n,i,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
 assert hit and o.name==water.name,(j,o.name if o else None)
 assert 2.00<loc.z<2.04
 rays.append([x,y,loc.z])
 for dx in [-.1,.1]:
  hit,loc,n,i,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x+dx,y,4)),Vector((0,0,-1)))
  assert hit and o.name==water.name,('Water clearance width',j,dx)
# Compare independent reopened baseline pivot transforms.
actual={n:list(bpy.data.objects[n].matrix_local[i][j] for i in range(4) for j in range(4)) for n in ['Lid_Hinge','Latch_Pivot']}
report={'status':'PASS','negative_detached_water_rejected':negative,'bank_peaks':peaks,'water_exposed_rays':rays,'terrain_lid_owned':True}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,values in actual.items():
 expected=[bpy.data.objects[n].matrix_local[i][j] for i in range(4) for j in range(4)]
 assert max(abs(a-b) for a,b in zip(values,expected))<1e-7,(n,values,expected)
report['baseline_pivots_match']=True
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print('THEME PASS',json.dumps(report))
