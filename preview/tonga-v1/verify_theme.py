import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'tonga.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']; latch=bpy.data.objects['Latch_Pivot']
def gate():
 diamonds=[o for o in bpy.data.objects if o.name.startswith('Lid / diamond')]
 assert len(diamonds)==6
 assert all(o.parent==lid for o in diamonds)
 for o in diamonds:
  pts=[o.matrix_world@v.co for v in o.data.vertices]
  extent=[max(v[i] for v in pts)-min(v[i] for v in pts) for i in range(3)]
  assert all(abs(a-b)<1e-5 for a,b in zip(extent,[.66,.54,.025])),extent
 assert all(o.parent==lid for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Lid /','Corner hardware /')))
 slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,[3.72,2.38,.30]))
 assert len([i for i in bpy.data.images if i.packed_file])>=3
 return True
gate()
# Real negative control: detach a diamond, verify the same oracle rejects it.
o=bpy.data.objects['Lid / diamond 0'];o.parent=None
try:gate();raise RuntimeError('Negative control unexpectedly passed')
except AssertionError:negative=True
o.parent=lid;gate()
pivots={o.name:[list(row) for row in o.matrix_local] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(pivots[n][i][j]-bpy.data.objects[n].matrix_local[i][j]) for n in pivots for i in range(4) for j in range(4));assert error<1e-7
result={'status':'PASS','six_hollow_raised_diamonds':True,'lid_ancestry':True,'dimensions':True,'packed_maps':True,'detached_ornament_negative_control_rejected':negative,'inherited_pivot_max_error':error}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
