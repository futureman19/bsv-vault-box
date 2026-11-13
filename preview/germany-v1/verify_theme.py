"""Independent saved-source contract plus deliberate failing ancestry control."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'germany.blend'),use_scripts=False)
bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7,n
lid=bpy.data.objects['Lid_Hinge']
def ancestry(o):
 p=o.parent
 while p:
  if p==lid:return True
  p=p.parent
 return False
village=[o for o in bpy.data.objects if o.name.startswith('Village /')]
assert village
for o in village:assert ancestry(o),o.name
trees=[o for o in village if o.name.startswith('Village / turned tree')]
assert len(trees)==3
assert len([o for o in village if o.name.startswith('Village / house')])==2
assert len([o for o in village if o.name.startswith('Village / roof')])==2
for o in trees:
 zs=[(o.matrix_world@v.co).z for v in o.data.vertices];assert abs(min(zs)-2.04)<1e-5 and max(zs)<2.95
# Ray from each root bottom onto the base alone, not hidden by foliage.
base=bpy.data.objects['Village / oval base'];roots=[]
for o in trees:
 coords=[o.matrix_world@v.co for v in o.data.vertices];low=min(v.z for v in coords);root=[v for v in coords if abs(v.z-low)<1e-5];x=sum(v.x for v in root)/len(root);y=sum(v.y for v in root)/len(root)
 origin=base.matrix_world.inverted()@Vector((x,y,2.05));direction=base.matrix_world.inverted().to_3x3()@Vector((0,0,-1));hit,loc,normal,face=base.ray_cast(origin,direction)
 assert hit
 world=base.matrix_world@loc;assert abs(world.z-low)<1e-5;roots.append({'tree':o.name,'base_hit_z':world.z,'root_z':low})
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
# Negative test is post-implementation regression evidence, not claimed test-first.
o=trees[0];saved=o.parent;o.parent=None
try:
 assert ancestry(o),'detached ornament lacks lid ancestry'
except AssertionError as e:negative={'status':'EXPECTED_FAIL','message':str(e)}
else:raise AssertionError('ancestry negative control incorrectly passed')
o.parent=saved
assert ancestry(o)
report={'status':'PASS','pivot_transforms_unchanged':True,'village_meshes':len(village),'turned_trees':len(trees),'houses':2,'roofs':2,'lid_ancestry':True,'root_contacts':roots,'slab_dimensions':list(slab.dimensions),'negative_control':negative}
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
