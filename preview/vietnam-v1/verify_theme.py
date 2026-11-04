import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'vietnam.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in baseline.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-7
islands=[o for o in bpy.data.objects if o.name.startswith('Karst island /')];assert len(islands)==5
lid=bpy.data.objects['Lid_Hinge'];water=bpy.data.objects['Bay / emerald water'];assert water.parent==lid
records=[]
def check(o):
 assert o.parent==lid, 'Island must belong to moving lid'
 verts=[o.matrix_world@v.co for v in o.data.vertices]
 lo=[min(v[i] for v in verts) for i in range(3)];hi=[max(v[i] for v in verts) for i in range(3)]
 assert lo[0]>-1.57 and hi[0]<1.57 and lo[1]>-.92 and hi[1]<.92
 assert 1.999<lo[2]<2.011 and .30<hi[2]-2.006<=.68, ('Island height outside frozen brief',o.name,hi[2]-2.006)
 assert any(f.material_index==1 for f in o.data.polygons)
 return {'name':o.name,'min':lo,'max':hi,'crown_faces':sum(f.material_index==1 for f in o.data.polygons)}
for o in islands:records.append(check(o))
# Genuine post-implementation negative control, never described as test-first.
o=islands[0];o.parent=None
try:check(o)
except AssertionError as e:negative=str(e)
else:raise AssertionError('Detached ornament incorrectly accepted')
o.parent=lid
assert negative=='Island must belong to moving lid'
# Independent horizontal footprint disjointness, beyond moving/static collision gate.
for i,a in enumerate(records):
 for b in records[i+1:]:assert a['max'][0]<b['min'][0] or b['max'][0]<a['min'][0] or a['max'][1]<b['min'][1] or b['max'][1]<a['min'][1]
r={'status':'PASS','islands':records,'original_pivot_matrices_unchanged':True,'island_footprints_disjoint':True,'negative_control_rejected':negative,'negative_control_kind':'post-implementation detached island'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r))
