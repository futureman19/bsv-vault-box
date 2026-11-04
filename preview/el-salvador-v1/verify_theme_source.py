import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'el-salvador.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];crater=bpy.data.objects['Terrain / volcanic crater'];water=bpy.data.objects['Terrain / turquoise lagoon']
def ancestry(o):
 assert o.parent==lid,'Detached terrain'
ancestry(crater);ancestry(water)
# Exercise the actual ancestry predicate with a detached object, then restore.
p=crater.parent;crater.parent=None
try:
 ancestry(crater)
 raise RuntimeError('negative control did not reject')
except AssertionError:negative=True
finally:crater.parent=p
bpy.context.view_layer.update()
vs=[crater.matrix_world@v.co for v in crater.data.vertices]
assert min(v.z for v in vs)<=1.978 and min(v.z for v in vs)>=1.97
assert 2.4<max(v.z for v in vs)<2.7
assert all(abs(v.x)<1.36 and -.78<v.y<1.02 for v in vs)
hits=[]
for x,y in [(0,.12),(.15,.12),(-.15,.12),(0,.22),(0,.02)]:
 hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
 assert hit and obj==water,(x,y,obj.name if obj else None)
 hits.append(list(loc))
# Compare exact inherited pivots against separately loaded baseline.
actual={n:[list(row) for row in bpy.data.objects[n].matrix_local] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,mat in actual.items():
 assert max(abs(mat[i][j]-bpy.data.objects[n].matrix_local[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','terrain_parentage':True,'detached_negative_control_rejected':negative,'crater_bounds':[[min(v[i] for v in vs),max(v[i] for v in vs)] for i in range(3)],'lagoon_downward_rays':hits,'inherited_pivots_unchanged':True}
(R/'theme-source-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
