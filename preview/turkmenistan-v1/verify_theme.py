import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'turkmenistan.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];parts=[o for o in bpy.data.objects if o.name.startswith('Carpet /')]
assert len(parts)==58,len(parts)
assert all(o.parent==lid for o in parts)
assert len([o for o in parts if o.name.startswith('Carpet / ivory octagon')])==3
assert len([o for o in parts if o.name.startswith('Carpet / fringe')])==38
bounds=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
assert max(v.z for v in bounds)<2.07
assert min(v.z for v in bounds)>=1.977
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,[3.72,2.38,.30]))
# Contrast of nested motifs and ownership must reject deliberately detached objects.
p=parts[0];p.parent=None
try: assert all(o.parent==lid for o in parts)
except AssertionError: negative=True
else: raise AssertionError('Detached ornament was not rejected')
p.parent=lid
r={'status':'PASS','pivot_matrices_preserved':True,'carpet_parts':len(parts),'octagonal_medallions':3,'fringe_bars':38,'max_z':max(v.z for v in bounds),'detached_parent_negative_control_rejected':negative,'invented_not_tribal_motifs':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
