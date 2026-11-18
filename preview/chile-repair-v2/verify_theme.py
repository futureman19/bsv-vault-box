"""Independent saved-source theme checks and deliberate in-memory negatives."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'chile.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
for n,rows in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-7

def bounds(o):
 points=[o.matrix_world@Vector(v) for v in o.bound_box]
 return [[min(v[k] for v in points),max(v[k] for v in points)] for k in range(3)]
def theme():
 basin=bpy.data.objects['Salt basin / bed'];bb=bounds(basin)
 assert bb[0][1]-bb[0][0]>=.7 and bb[1][1]-bb[1][0]>=.45,'basin size'
 themed=[o for o in bpy.data.objects if o.name.startswith(('Salt ','Ridge /','Terrain /')) and o.type=='MESH']
 assert all(o.parent==lid for o in themed),'lid ownership'
 ridges=[o for o in themed if o.name.startswith('Ridge /')];assert len(ridges)==2
 relief=[bounds(o)[2][1]-1.978 for o in ridges];assert all(.35<=h<=.75 for h in relief),'ridge relief'
 assert len([o for o in themed if o.name.startswith('Salt crust /')])>=15
 assert not any(any(s in o.name.lower() for s in ['cedar','moss','glacier']) for o in bpy.data.objects)
 return {'basin_bounds':bb,'ridge_relief':relief,'ornament_meshes':len(themed),'lid_ancestry':True}
report=theme();negative=[]
basin=bpy.data.objects['Salt basin / bed'];mw=basin.matrix_world.copy();basin.parent=None
try:theme()
except AssertionError as e:negative.append('detached basin rejected: '+str(e))
else:raise AssertionError('negative ancestry did not fail')
basin.parent=lid;basin.matrix_world=mw;bpy.context.view_layer.update()
scale=basin.scale.copy();basin.scale.x=.05;bpy.context.view_layer.update()
try:theme()
except AssertionError as e:negative.append('undersized basin rejected: '+str(e))
else:raise AssertionError('negative size did not fail')
basin.scale=scale;bpy.context.view_layer.update();theme()
# Salt foreground visible from the source camera: sample rays to known basin points.
cam=bpy.context.scene.camera;dep=bpy.context.evaluated_depsgraph_get();hits=[]
for x,y in [(-.7,-.4),(-.3,-.4),(.2,-.35)]:
 target=Vector((x,y,2.08));direction=(target-cam.location).normalized();hit,loc,n,i,obj,m=bpy.context.scene.ray_cast(dep,cam.location,direction)
 hits.append(obj.name if hit else None)
assert all(n and n.startswith('Salt ') for n in hits),hits
report.update(status='PASS',same_family_pivots=True,negative_controls=negative,source_camera_salt_visibility_hits=hits,scope='Source-camera point rays, not complete visibility or geographic proof')
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print('THEME PASS',json.dumps(report))
