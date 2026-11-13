"""Independent source geometry/parentage and negative-control checks."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mauritania.blend'),use_scripts=False)
o=bpy.data.objects['Terrain / Richat three cuestas and dunes'];lid=bpy.data.objects['Lid_Hinge']
assert o.parent==lid
bpy.context.view_layer.update()
points=[o.matrix_world@v.co for v in o.data.vertices]
def ring_check(pts):
 # Sample three crest/valley pairs along a ray away from both erosion channels.
 theta=1.15
 def height(r):
  x=1.31*r*math.cos(theta);y=.83*r*math.sin(theta)
  return min(pts,key=lambda v:(v.x-x)**2+(v.y-y)**2).z
 crests=[height(r) for r in [.29,.53,.79]];valleys=[height(r) for r in [.40,.65,.96]]
 assert all(a-b>.07 for a,b in zip(crests,valleys)),(crests,valleys)
 assert .12<max(p.z for p in pts)-1.978<.40
 return {'crest_heights':crests,'valley_heights':valleys,'max_relief':max(p.z for p in pts)-1.978}
result=ring_check(points)
flat=[Vector((p.x,p.y,1.995)) for p in points]
try:ring_check(flat)
except AssertionError:result['flattened_geometry_negative_control_rejected']=True
else:raise AssertionError('Theme validator accepted missing relief')
assert all(p.z>=1.978 for p in points)
result.update(status='PASS',terrain_vertices=len(points),lid_parent=o.parent.name,negative_control='Post-implementation flattened-geometry control; not test-first TDD',source='Saved blend reopened independently')
(R/'theme-source-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
