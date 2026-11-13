import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'oman.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Terrace /','Falaj /'))]
def ancestry():assert len(ornaments)==15 and all(o.parent==lid for o in ornaments)
ancestry();o=ornaments[0];o.parent=None
try:ancestry()
except AssertionError:negative=True
else:raise AssertionError('Detached ornament was not rejected')
o.parent=lid;bpy.context.view_layer.update();ancestry()
gardens=[o for o in ornaments if 'garden' in o.name];assert len(gardens)==6
bounds=[]
for o in ornaments:
 points=[o.matrix_world@Vector(c) for c in o.bound_box]
 assert all(abs(v.x)<1.4 and abs(v.y)<.95 for v in points)
 bounds.append({'name':o.name,'min_z':min(v.z for v in points),'max_z':max(v.z for v in points)})
for o in gardens:
 top=max((o.matrix_world@Vector(c)).z for c in o.bound_box)
 assert min(abs(top-z) for z in [2.118,2.238,2.358])<1e-5
rays=[]
for y in [-.75,-.5,-.25,0,.25,.5,.75]:
 hit,loc,n,idx,obj,mat=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((0,y,3)),Vector((0,0,-1)))
 assert hit and obj.name=='Falaj / continuous water';rays.append(list(loc))
# Exact inherited pivots from independent saved source, not names alone.
actual={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
for n,v in actual.items():assert max(abs(a-b) for a,b in zip(v,bpy.data.objects[n].location))<1e-7
out={'status':'PASS','ornaments':len(ornaments),'garden_beds':len(gardens),'bounds':bounds,'water_exposed_rays':rays,'detached_negative_control_rejected':negative,'inherited_pivots':actual}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('PASS theme, exposed falaj, negative ancestry control, original pivots')
