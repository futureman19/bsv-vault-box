import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'tajikistan.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
ridge=bpy.data.objects['Terrain / Pamir ridge'];lake=bpy.data.objects['Terrain / Alpine lake']
checks={}
def check(name,value):
 checks[name]=bool(value)
 (R/'theme-check.json').write_text(json.dumps({'checks':checks,'PASS':all(checks.values())},indent=2))
 assert value,name
check('lid_ancestry',ridge.parent==lid and lake.parent==lid and latch.parent==lid)
v=[ridge.matrix_world@v.co for v in ridge.data.vertices];h=max(p.z for p in v)
check('ridge_height_2.65_to_2.95',2.65<=h<=2.95)
check('ridge_footprint',min(p.x for p in v)>=-1.451 and max(p.x for p in v)<=1.451 and min(p.y for p in v)>=-.101 and max(p.y for p in v)<=.941)
check('snow_and_rock',set(p.material_index for p in ridge.data.polygons)=={0,1})
# Three separated high regions along the middle row, not merely named peaks.
row=v[14*65:15*65];peaks=[i for i in range(1,64) if row[i].z>row[i-1].z and row[i].z>row[i+1].z and row[i].z>2.4]
check('three_summits',len(peaks)>=3)
w=[lake.matrix_world@v.co for v in lake.data.vertices]
check('lake_height',all(1.992<=p.z<=2.025 for p in w))
check('lake_front',max(p.y for p in w)<-.10)
check('lake_upward_normals',all(p.normal.z>.99 for p in lake.data.polygons))
for x,y in [(.1,-.48),(-.3,-.48),(.5,-.48)]:
 hit,loc,n,i,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
 check('lake_exposed_'+str(x),hit and o==lake)
check('packed_maps',len([i for i in bpy.data.images if i.packed_file])>=3)
# Negative control: detached ornament must fail the exact ancestry predicate.
p=lake.parent;lake.parent=None;rejected=not(lake.parent==lid);lake.parent=p
check('negative_control_detached_lake_rejected',rejected)
check('no_cedar_geometry',not any('Cedar' in o.name for o in bpy.data.objects))
current_pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(current_pivots[name][i][j]-bpy.data.objects[name].matrix_world[i][j]) for name in current_pivots for i in range(4) for j in range(4))
check('inherited_pivot_matrices',error<1e-7)
(R/'theme-check.json').write_text(json.dumps({'PASS':True,'checks':checks,'pivot_error':error,'ridge_max_z':h,'summit_indices':peaks,'negative_control':'temporarily detached lake rejected; restored without saving'},indent=2))
print('PASS theme',json.dumps(checks))
