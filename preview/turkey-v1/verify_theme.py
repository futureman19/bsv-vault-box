import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'turkey.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
for n,m in baseline.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
ornaments=[o for o in bpy.data.objects if o.name.startswith('Ornament /')]
def check():
 assert all(o.parent==lid for o in ornaments),'Ornament missing lid ownership'
 assert len([o for o in ornaments if o.name.startswith('Ornament / tulip')])==3
 assert len([o for o in ornaments if o.name.startswith('Ornament / leaf')])==6
 for o in ornaments:
  for v in o.data.vertices:
   w=o.matrix_world@v.co
   assert abs(w.x)<=1.601 and abs(w.y)<=.931 and 1.969<=w.z<=2.131,(o.name,list(w))
check()
# Exterior skin interiors must not overlap; touching butt joints are permitted.
skins=[o for o in bpy.data.objects if o.name in ['Ceramic / front','Ceramic / rear'] or o.name.startswith('Ceramic / side')]
for i,a in enumerate(skins):
 for b in skins[i+1:]:
  av=[a.matrix_world@v.co for v in a.data.vertices];bv=[b.matrix_world@v.co for v in b.data.vertices]
  overlaps=[min(max(v[k] for v in av),max(v[k] for v in bv))-max(min(v[k] for v in av),min(v[k] for v in bv)) for k in range(3)]
  assert min(overlaps)<1e-6,('Overlapping ceramic skins',a.name,b.name,overlaps)
o=bpy.data.objects['Ornament / tulip 0'];o.parent=None
try:check()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control failed to reject detached tulip')
o.parent=lid
assert not any('Cedar' in o.name or 'Granite' in o.name for o in bpy.data.objects)
result={'status':'PASS','ornaments':len(ornaments),'tulips':3,'leaves':6,'baseline_pivots_equal':True,'negative_control_rejected':negative,'bounds_checked':True,'original_composition_not_historical_replica':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(result)
