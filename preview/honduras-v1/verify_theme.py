import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'honduras.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Terrain /','Rainforest /','River /'))]
def owned():return all(o.parent==lid for o in ornaments)
assert owned();o=ornaments[0];o.parent=None;assert not owned();o.parent=lid;bpy.context.view_layer.update()
canopies=[o for o in ornaments if 'canopy' in o.name];assert len(canopies)>=12
bounds=[o.matrix_world@v.co for o in ornaments for v in o.data.vertices]
assert max(v.z for v in bounds)<2.778 and max(abs(v.x) for v in bounds)<1.6 and max(abs(v.y) for v in bounds)<1.1
hits=[]
for i in range(61):
 y=-.92+i*1.84/60;x=.26*math.sin(4*y)+.12*y
 hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
 hits.append(bool(hit and obj.name=='River / continuous meander'))
assert all(hits),hits
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
assert all(max(abs(bpy.data.objects[n].matrix_world[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-7 for n,rows in pivots.items())
r={'status':'PASS','lid_owned_ornaments':len(ornaments),'canopies':len(canopies),'river_centerline_exposed_samples':len(hits),'detached_ornament_negative_control':'REJECTED as expected','inherited_pivots_equal':True,'relief_max_z':max(v.z for v in bounds)}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
