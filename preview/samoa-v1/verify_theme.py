import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'samoa.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def bounds(o):
 vs=[o.matrix_world@v.co for v in o.data.vertices]
 return [[min(v[a] for v in vs) for a in range(3)],[max(v[a] for v in vs) for a in range(3)]]
cloth=bpy.data.objects['Siapo / lid cloth'];rocks=[o for o in bpy.data.objects if o.name.startswith('Lava / lid mound')]
def ownership():
 assert cloth.parent==lid and len(rocks)==3 and all(o.parent==lid for o in rocks),'Detached ornament'
ownership();cb=bounds(cloth)
assert abs(cb[1][0]-cb[0][0]-3.16)<1e-5 and abs(cb[1][1]-cb[0][1]-1.88)<1e-5
top_z=[(cloth.matrix_world@v.co).z for v in cloth.data.vertices[:33*21]]
assert min(top_z)>=2.01 and max(top_z)<=2.07,('Cloth top outside brief',min(top_z),max(top_z))
assert 2.00<cb[1][2]<2.07 and cb[0][2]<1.98
rb=[bounds(o) for o in rocks];assert max(b[1][2] for b in rb)<2.40
assert len([o for o in bpy.data.objects if o.name.startswith('Siapo / body panel')])==2
assert len([o for o in bpy.data.objects if o.name.startswith('Siapo / side panel')])==2
original=cloth.parent;cloth.parent=None
try:ownership()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control failed to reject')
cloth.parent=original
# Independently evaluate original saved mechanism pivot transforms.
actual={o.name:[list(row) for row in o.matrix_local] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,matrix in actual.items():
 base=bpy.data.objects[name].matrix_local
 assert max(abs(base[i][j]-matrix[i][j]) for i in range(4) for j in range(4))<1e-7
r=dict(status='PASS',cloth_top_z=[min(top_z),max(top_z)],cloth_bounds=cb,lava_bounds=rb,lid_ornaments=4,body_panels=4,negative_control_rejected=negative,pivots_match_included_mechanism=True)
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
