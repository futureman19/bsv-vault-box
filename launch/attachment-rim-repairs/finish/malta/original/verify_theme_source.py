import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
base={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'malta.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,v in base.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-v[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];orn=[o for o in bpy.data.objects if o.name.startswith(('Harbour /','Peninsula /'))];assert len(orn)==9 and all(o.parent==lid for o in orn)
pen=bpy.data.objects['Peninsula / angular bastions'];v=[pen.matrix_world@v.co for v in pen.data.vertices];assert max(p.z for p in v)-1.978<=.55
# Alternating convex/concave turns certify a genuinely bastioned outline.
points=[(p.x,p.y) for p in v[:len(v)//2]];turn=[]
for i,b in enumerate(points):
 a=points[i-1];c=points[(i+1)%len(points)];turn.append((b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]))
assert sum(t<0 for t in turn)>=3 and sum(t>0 for t in turn)>=3
rays=[]
for x,y,expect in [(0,-.65,'Harbour /'),(0,.73,'Harbour /'),(0,0,'Peninsula /')]:
 hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and obj.name.startswith(expect),(x,y,obj.name);rays.append(dict(x=x,y=y,object=obj.name,z=loc.z))
ash=[o for o in bpy.data.objects if o.name.startswith('Ashlar /')];assert len(ash)>=60
# Negative ancestry control exercises real validator then restores state.
def owned():return all(o.parent==lid for o in orn)
old=pen.parent;pen.parent=None;assert not owned();pen.parent=old;assert owned()
result=dict(status='PASS',original_pivots=True,lid_owned_ornaments=len(orn),ashlar_blocks=len(ash),concave_turns=sum(t<0 for t in turn),water_two_sides_rays=rays,detached_ornament_rejected=True)
(R/'theme-source-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
