import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
names=['Lid_Hinge','Latch_Pivot']
base={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in names}
bpy.ops.wm.open_mainfile(filepath=str(R/'eritrea.blend'),use_scripts=False);bpy.context.view_layer.update()
for n in names: assert base[n]==[list(r) for r in bpy.data.objects[n].matrix_world]
islands=[o for o in bpy.data.objects if o.name.startswith('Island /')]
def owned(items):return len(items)>=5 and all(o.parent and o.parent.name=='Lid_Hinge' for o in items)
assert owned(islands)
o=islands[0];parent=o.parent;o.parent=None;assert not owned(islands);o.parent=parent
bounds={o.name:[min((o.matrix_world@Vector(c)).z for c in o.bound_box),max((o.matrix_world@Vector(c)).z for c in o.bound_box)] for o in islands}
assert all(1.98<=a<2.0 and b-1.9935<.35 for a,b in bounds.values())
assert all(abs(o.dimensions.z-.09)<1e-6 for o in bpy.data.objects if o.name.startswith('Seam /'))
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
r=dict(status='PASS',unchanged_pivots=base,island_world_z=bounds,seam_height=.09,detached_island_negative_rejected=True)
(R/'contract-check.json').write_text(json.dumps(r,indent=2));print('CONTRACT_PASS')
