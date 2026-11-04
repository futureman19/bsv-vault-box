"""Independent saved-source visual-contract checks; not perceptual equivalence."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'central-african-republic.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def check():
 assert latch.parent==lid
 assert abs(lid.location.y-1.32)<1e-5 and abs(lid.location.z-1.668)<1e-5
 landscape=[o for o in bpy.data.objects if o.name.startswith('Landscape /')]
 canopy=[o for o in landscape if 'canopy' in o.name];trunks=[o for o in landscape if 'trunk' in o.name]
 assert len(canopy)==35 and len(trunks)==7
 assert all(o.parent==lid for o in landscape)
 verts=[o.matrix_world@v.co for o in landscape for v in o.data.vertices]
 assert all(abs(v.x)<1.65 and abs(v.y)<1.15 and 1.97<v.z<2.83 for v in verts)
 slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.001 and abs(slab.dimensions.y-2.38)<.001
 for o in bpy.data.objects:
  if o.name.startswith('Mineral seam'):assert o.dimensions.z<.12
 assert 'Landscape / sandy clearing' in bpy.data.objects and 'Landscape / water inset' in bpy.data.objects
 assert not any('Cedar' in o.name or 'glacier' in o.name for o in bpy.data.objects)
 return {'landscape_meshes':len(landscape),'canopy_lobes':len(canopy),'broadleaf_trunks':len(trunks),'max_height':max(v.z for v in verts),'lid_width':slab.dimensions.x,'lid_depth':slab.dimensions.y}
bpy.context.view_layer.update();result=check()
# Deliberate in-memory parent corruption must fail; never save this invalid source.
o=bpy.data.objects['Landscape / canopy 0 0'];saved=o.parent;o.parent=None
try:check()
except AssertionError:negative=True
else:raise AssertionError('Theme gate failed to reject detached canopy')
o.parent=saved;bpy.context.view_layer.update();check()
result.update(status='PASS',detached_canopy_negative_control_rejected=negative,scope='geometry and parentage; source saved before test; not visual realism')
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
