import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'dominica.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];lake=bpy.data.objects['Lake / geothermal water'];ridges=[o for o in bpy.data.objects if o.name.startswith('Rainforest / ridge')];canopy=[o for o in bpy.data.objects if o.name.startswith('Rainforest / canopy')]
def check_ownership():
 for o in [lake,bpy.data.objects['Lake / rocky rim']]+ridges+canopy:assert o.parent==lid,('Detached terrain',o.name)
check_ownership();lake.parent=None
try:check_ownership()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control did not fail')
lake.parent=lid
# Reload rather than depend on parent reassignment transforms.
bpy.ops.wm.open_mainfile(filepath=str(R/'dominica.blend'),use_scripts=False);bpy.context.view_layer.update();lake=bpy.data.objects['Lake / geothermal water'];lid=bpy.data.objects['Lid_Hinge']
assert len(ridges)==5 and len(canopy)>65
coords=[lake.matrix_world@v.co for v in lake.data.vertices];lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)]
assert abs(lo[0]+.72)<1e-5 and abs(hi[0]-.42)<1e-5 and abs(hi[2]-2.08)<1e-5
# Vertical rays prove visible lake aperture, not merely overlapping bounding boxes.
water_hits=0
for x in [-.45,-.15,.15]:
 for y in [-.45,-.28,-.11]:
  hit,loc,n,idx,obj,mat=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
  assert hit and obj.name==lake.name,('Lake occluded',x,y,obj.name);water_hits+=1
# Saved source pivots compared against independent evaluated mechanism.
record={n: {'matrix':[list(row) for row in bpy.data.objects[n].matrix_world], 'parent':bpy.data.objects[n].parent.name if bpy.data.objects[n].parent else None} for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,r in record.items():
 assert max(abs(r['matrix'][i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','ridge_count':len(ridges),'canopy_count':len(canopy),'lake_bounds':[lo,hi],'lake_visible_vertical_rays':water_hits,'terrain_lid_ownership':True,'detached_lake_negative_control':negative,'original_pivots_match':True}
(R/'theme-source-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
