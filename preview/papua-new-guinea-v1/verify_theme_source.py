import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'papua-new-guinea.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in baseline.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
ridges=[o for o in bpy.data.objects if o.name.startswith('Highland ridge /')]
def validate_ridges(items):
 assert len(items)==3
 for o in items:
  assert o.parent and o.parent.name=='Lid_Hinge',o.name
  v=[o.matrix_world@x.co for x in o.data.vertices]
  assert .35<max(x.z for x in v)-1.978<.65
  assert min(x.z for x in v)<1.978<max(x.z for x in v)
 vs=[o.matrix_world@v.co for o in items for v in o.data.vertices]
 assert max(v.x for v in vs)-min(v.x for v in vs)<=2.6
 assert max(v.y for v in vs)-min(v.y for v in vs)<=1.45
validate_ridges(ridges)
o=ridges[0];p=o.parent;o.parent=None
try:
 validate_ridges(ridges)
except AssertionError:negative=True
else:raise AssertionError('Detached ridge was not rejected')
o.parent=p
panels=[o for o in bpy.data.objects if o.name.startswith('Fibre panel')];assert len(panels)==4
assert not any('Cedar' in o.name or 'Granite' in o.name for o in bpy.data.objects)
r={'status':'PASS','ridges':3,'fibre_panels':4,'pivot_matrices_unchanged':True,'relief_height_and_footprint':True,'negative_detached_ridge_rejected':negative,'note':'Post-implementation negative control, not test-first history.'}
(R/'theme-source-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
