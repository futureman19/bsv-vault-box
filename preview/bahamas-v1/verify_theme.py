import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(v) for v in bpy.data.objects[n].matrix_local] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'bahamas.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
for n,rows in pivots.items():assert max(abs(bpy.data.objects[n].matrix_local[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-7
orn=[o for o in bpy.data.objects if o.name.startswith(('Pink shore','Blue hole','Lagoon'))]
assert len(orn)==5

def owned():assert all(o.parent==lid for o in orn),'Detached lid ornament'
owned();o=orn[0];mw=o.matrix_world.copy();o.parent=None
try:owned()
except AssertionError as e:negative={'detached_ornament_rejected':True,'message':str(e)}
else:raise AssertionError('Ancestry gate cannot fail')
o.parent=lid;o.matrix_world=mw;bpy.context.view_layer.update();owned()
bounds={}
for o in orn:
 v=[o.matrix_world@p.co for p in o.data.vertices];bounds[o.name]={'min':[min(p[i] for p in v) for i in range(3)],'max':[max(p[i] for p in v) for i in range(3)]}
 assert all(abs(p.x)<1.63 and abs(p.y)<.96 and 1.97<=p.z<2.28 for p in v)
# Downward rays prove visible blue center, turquoise outside and pink bank.
rays=[]
for x,y,prefix in [(.55,.12,'Blue hole / deep center'),(.55,-.40,'Lagoon'),(-.72,-.22,'Pink shore')]:
 hit,loc,norm,idx,obj,mat=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and obj.name.startswith(prefix),(x,y,obj.name)
 rays.append({'xy':[x,y],'object':obj.name,'height':loc.z})
assert not any(o.name.startswith(('Cedar','Terrain / moss','Finger')) for o in bpy.data.objects)
r={'status':'PASS','unchanged_mechanical_pivots':True,'lid_ornaments':len(orn),'bounds':bounds,'visible_surface_rays':rays,'negative_control':negative,'note':'post-implementation negative control; not test-first TDD'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
