import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'micronesia.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
for n,rows in baseline.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-7
platforms=[o for o in bpy.data.objects if o.name.startswith('Islet / platform')]
relief=[o for o in bpy.data.objects if o.name.startswith(('Islet /','Lagoon /','Basalt enclosure /','Basalt relief /'))]
def ownership():assert all(o.parent==lid for o in relief),'Detached lid ornament'
assert len(platforms)==6;ownership()
# Genuine negative control: mutate ownership in memory, confirm the same gate rejects.
p=platforms[0];p.parent=None
try:ownership()
except AssertionError:negative=True
else:raise AssertionError('Ownership gate cannot fail')
p.parent=lid
bounds=[o.matrix_world@Vector(v) for o in relief for v in o.bound_box]
assert max(v.z for v in bounds)-1.978<.65
assert max(abs(v.x) for v in bounds)<1.7 and max(abs(v.y) for v in bounds)<1.0
assert len([o for o in bpy.data.objects if o.name.startswith('Basalt course /')])==112
assert not any(o.name.startswith(('Cedar tree','Terrain / moss')) for o in bpy.data.objects)
# Downward source geometry rays prove connected exposed canal cross, not only a named blue mesh.
dep=bpy.context.evaluated_depsgraph_get();hits=[]
for x,y in [(x*.1,-.06) for x in range(-14,15)]+[(v,y*.1) for v in [-.55,.51] for y in range(-8,9)]:
 hit,loc,n,i,obj,mat=bpy.context.scene.ray_cast(dep,Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and obj.name.startswith('Lagoon /'),(x,y,obj.name if hit else None)
 hits.append([x,y,float(loc.z)])
# Enclosure has an actual open center.
hit,loc,n,i,obj,mat=bpy.context.scene.ray_cast(dep,Vector((-1.02,.37,3)),Vector((0,0,-1)))
assert obj.name.startswith('Islet / platform')
out=dict(status='PASS',platforms=len(platforms),lid_relief_meshes=len(relief),relief_height=max(v.z for v in bounds)-1.978,basalt_courses=112,original_pivots=True,detached_ornament_negative_rejected=negative,exposed_connected_canal_samples=hits,open_enclosure_center=obj.name)
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
