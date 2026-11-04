import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'ethiopia.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
terrain=[o for o in bpy.data.objects if o.name.startswith('Escarpment /')]
assert len(terrain)==3
assert not any('Cedar' in o.name or 'glacier' in o.name.lower() for o in bpy.data.objects)
def owned():return all(o.parent==lid for o in terrain)
assert owned()
terrain[0].parent=None
assert not owned(),'negative control must fail'
terrain[0].parent=lid
bounds={}
for o in terrain:
 v=[o.matrix_world@v.co for v in o.data.vertices]
 lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
 assert abs(lo[2]-1.978)<1e-5 and 2.22<hi[2]<2.85
 assert lo[0]>-1.55 and hi[0]<1.55 and lo[1]>-.94 and hi[1]<.94
 bounds[o.name]={'min':lo,'max':hi}
# Both valley rays must reach the solid lid rather than a named terrain mass.
valleys=[]
for x,y in [(0,-.40),(.65,-.08)]:
 hit,loc,n,idx,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
 assert hit and o.name=='Lid / polished slab',(x,y,o.name)
 valleys.append({'xy':[x,y],'hit':o.name,'z':loc.z})
current={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,m in current.items():
 actual=bpy.data.objects[name].matrix_world
 assert max(abs(actual[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','terrain_count':3,'bounds':bounds,'valley_rays':valleys,'all_terrain_lid_owned':True,'detached_terrain_negative_control_rejected':True,'original_pivot_matrices_preserved':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
