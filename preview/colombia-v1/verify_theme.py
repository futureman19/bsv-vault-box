import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'colombia.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']; shrubs=[o for o in bpy.data.objects if o.name.startswith('Coffee shrub')];hill=bpy.data.objects['Cordillera / planted hills'];house=[o for o in bpy.data.objects if o.name.startswith('Farmhouse')]
def check():
 assert len(shrubs)>=36
 assert len(house)==4
 assert all(o.parent==lid for o in shrubs+house+[hill]),'ornament detached from lid'
 assert len(hill.data.vertices)>1000
 v=[hill.matrix_world@v.co for v in hill.data.vertices]
 bounds=[min(p[i] for p in v) for i in range(3)]+[max(p[i] for p in v) for i in range(3)]
 assert bounds[3]-bounds[0]<=2.9 and bounds[4]-bounds[1]<=1.7 and bounds[5]<2.628
 for n,a in pivots.items():
  assert max(abs(a[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
 for n in ['bamboo-color.png','bamboo-roughness.png','stone.png']:
  im=bpy.data.images[n];assert im.packed_file and max(im.size)<=512
 assert not any(o.name.startswith(('Cedar','Terrain / moss','Finger /')) for o in bpy.data.objects)
 return bounds
bounds=check()
# Post-implementation negative control: exercise the same ancestry oracle.
s=shrubs[0];s.parent=None
try:check()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control incorrectly accepted')
s.parent=lid;check()
r={'status':'PASS','shrubs':len(shrubs),'farmhouse_parts':len(house),'hill_bounds':bounds,'unchanged_pivot_matrices':True,'packed_maps':3,'negative_control_rejected':negative,'negative_control_type':'post-implementation deliberate detached ornament; not test-first history'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
