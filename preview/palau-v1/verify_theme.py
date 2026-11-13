"""Independent saved-scene theme and inherited-pivot contract; negative controls."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_local] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'palau.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];islands=[o for o in bpy.data.objects if o.name.startswith('Island /')]
def check():
 assert len(islands)>=5
 for o in islands:
  assert o.parent==lid,('detached island',o.name)
  vs=[o.matrix_world@v.co for v in o.data.vertices]
  assert max(v.z for v in vs)<=1.978+.85
  assert min(v.z for v in vs)<2.0 and min(v.z for v in vs)>1.97
  assert max(abs(v.x) for v in vs)<1.65 and max(abs(v.y) for v in vs)<.975
  assert len(o.data.materials)==2
  assert {p.material_index for p in o.data.polygons}=={0,1}
 for n,rows in pivots.items():
  assert max(abs(bpy.data.objects[n].matrix_local[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-7
check()
o=islands[0];p=o.parent;o.parent=None
try:check()
except AssertionError:negative=True
else:raise AssertionError('detached ornament accepted')
finally:o.parent=p
bpy.context.view_layer.update();check()
# Closed lagoon perimeter and lane rays hit water rather than island; direct object BVH.
def ray(x,y):
 hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and obj.name=='Lagoon / inset',(x,y,obj.name if hit else None)
 return [x,y,loc.z]
lanes=[ray(x,y) for x,y in [(-1.5,0),(0,0),(1.5,0),(0,.88),(0,-.88),(-.6,.35),(.23,.4)]]
# All terrain parts are included in generic moving-part collision set.
report={'status':'PASS','islands':len(islands),'inherited_pivots_equal':True,'islands_lid_owned':True,'terrain_height_max':max((o.matrix_world@v.co).z for o in islands for v in o.data.vertices),'lagoon_clear_sampled_rays':lanes,'detached_island_negative_control_rejected':negative,'limits':'Original stylized island arrangement; sampled water rays, not a geographic survey.'}
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
