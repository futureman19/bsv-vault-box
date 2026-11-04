"""Independent saved-source shape/attachment/negative-space contract."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'paraguay.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
orn=[o for o in bpy.data.objects if o.name.startswith('Sunlace /')]
def owned(o):
 p=o.parent
 while p:
  if p==lid:return True
  p=p.parent
 return False
assert orn and all(owned(o) for o in orn)
o=orn[0];p=o.parent;o.parent=None
rejected=not all(owned(q) for q in orn);o.parent=p
assert rejected
counts={}
for k in range(5):
 group=[o for o in orn if o.name.startswith(f'Sunlace / rosette {k} ')]
 counts[k]={s:len([o for o in group if s in o.name]) for s in ['ring','spoke','petal']}
 assert counts[k]==dict(ring=4,spoke=24 if k==0 else 16,petal=12 if k==0 else 8)
# Rays through central ring centre and spoke gaps must reach backing, not opaque decoration.
dep=bpy.context.evaluated_depsgraph_get();rays=[]
for cx,cy,rad in [(0,0,.64),(-1.08,-.56,.30),(1.08,-.56,.30),(-1.08,.56,.30),(1.08,.56,.30)]:
 hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(dep,Vector((cx,cy,2.4)),Vector((0,0,-1)))
 assert hit and obj.name=='Lid / polished slab',(cx,cy,obj.name)
 rays.append({'xy':[cx,cy],'surface':obj.name,'z':loc.z})
verts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
zmin=min(v.z for v in verts);zmax=max(v.z for v in verts)
assert 1.97<zmin<1.99 and 2.005<zmax<2.08,(zmin,zmax)
# Compare pivots directly to the preserved trimmed source, evaluating each scene separately.
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(pivots[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in pivots for i in range(4) for j in range(4))
assert err<1e-6,err
result=dict(status='PASS',rosettes=counts,ornament_meshes=len(orn),lid_ownership=True,detached_ornament_negative_control_rejected=rejected,openwork_centre_rays=rays,ornament_z=[zmin,zmax],pivot_max_error=err,limits='Invented radial decoration, not a traditional pattern replica; sampled rays do not measure textile authenticity.')
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
