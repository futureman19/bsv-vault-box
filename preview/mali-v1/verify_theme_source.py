import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mali.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];terrain=bpy.data.objects['Terrain / Bandiagara escarpment'];latch=bpy.data.objects['Latch_Pivot']
def check_parent():assert terrain.parent==lid,'detached terrain'
check_parent();terrain.parent=None
try:check_parent();raise RuntimeError('negative did not fail')
except AssertionError:negative=True
terrain.parent=lid;bpy.context.view_layer.update()
v=[terrain.matrix_world@x.co for x in terrain.data.vertices];bounds=[[min(p[i] for p in v),max(p[i] for p in v)] for i in range(3)]
assert 2.5<=bounds[0][1]-bounds[0][0]<=3.1
assert .65<=bounds[1][1]-bounds[1][0]<=1.2
assert .45<=bounds[2][1]-1.978<=.85
# Measure upper strata at three shoulder zones and intervening gullies.
def top(x):return max(p.z for p in v if abs(p.x-x)<.04)
shoulders=[top(x) for x in [-.95,0,.98]];gullies=[top(x) for x in [-.50,.61]]
assert len(set(round(z,2) for z in shoulders))==3
assert max(gullies)<min(shoulders)-.1
assert bounds[1][0]>0 and bounds[1][1]<1.10
# Reopen baseline independently and compare evaluated pivot world transforms.
current={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in current.items():assert max(abs(rows[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
out=dict(status='PASS',bounds=bounds,shoulder_heights=shoulders,gully_heights=gullies,detached_terrain_negative_rejected=negative,pivots_match_mechanism=True)
(R/'theme-source-check.json').write_text(json.dumps(out,indent=2));print(out)
