import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'lebanon.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];orn=[o for o in bpy.data.objects if o.name.startswith(('Lebanon cedar','Terrain / limestone'))]
def ancestry(objects):
 for o in objects:
  p=o.parent
  while p and p!=lid:p=p.parent
  assert p==lid,('Detached ornament',o.name)
ancestry(orn)
first=orn[0];old=first.parent;first.parent=None
try:ancestry(orn)
except AssertionError:negative=True
else:negative=False
first.parent=old;assert negative
canopy=[o for o in orn if 'canopy' in o.name or 'crown' in o.name]
verts=[o.matrix_world@v.co for o in canopy for v in o.data.vertices]
width=max(v.x for v in verts)-min(v.x for v in verts);height=max(v.z for v in verts)-1.978
assert len(canopy)==16 and .8<width<1.65 and .65<height<1.15,(len(canopy),width,height)
trunk=bpy.data.objects['Lebanon cedar / trunk'];v=[trunk.matrix_world@v.co for v in trunk.data.vertices];assert abs(sum(q.x for q in v)/len(v)-.55)<.25
bed=bpy.data.objects['Terrain / limestone root bed'];v=[bed.matrix_world@v.co for v in bed.data.vertices];assert min(q.z for q in v)<1.978<max(q.z for q in v) and max(q.z for q in v)-1.978<.22
assert len([o for o in orn if 'branch' in o.name])==15
assert len([o for o in bpy.data.objects if o.name.startswith('Limestone /')])==4
out={'status':'PASS','exact_base_pivots':True,'all_ornaments_lid_owned':len(orn),'canopy_pads':len(canopy),'canopy_width':width,'height_above_lid':height,'root_bed_intersects_lid':True,'detached_ornament_negative_control_rejected':negative,'limestone_wall_count':4}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
