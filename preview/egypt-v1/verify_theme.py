"""Independent saved-source contract; --negative-control proves rejection."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'egypt.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert latch.parent==lid
pyramids=[o for o in bpy.data.objects if o.name.startswith('Pyramid /')]
if '--negative-control' in sys.argv:pyramids[0].parent=None
assert len(pyramids)==3 and all(o.parent==lid for o in pyramids),'Three pyramids must travel with lid'
assert all(o.parent==lid for o in bpy.data.objects if o.name.startswith('Terrain /'))
assert not any(k in o.name for o in bpy.data.objects for k in ['Cedar','Moss','Glacier'])
sizes=sorted([tuple(o.dimensions) for o in pyramids],reverse=True)
assert .90<sizes[0][0]<.94 and .65<sizes[0][2]<.85
assert .64<sizes[1][0]<.68 and .38<sizes[2][0]<.42
for o in pyramids:
 for v in o.data.vertices:
  co=o.matrix_world@v.co
  assert abs(co.x)<1.5 and abs(co.y)<.95 and 1.97<co.z<2.9
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
assert abs(lid.location.y-1.32)<1e-5 and abs(lid.location.z-1.668)<1e-5
images=[i for i in bpy.data.images if i.packed_file];assert len(images)==3
assert all(max(i.size)<=1024 for i in images)
assert all(o.dimensions.z<.12 for o in bpy.data.objects if o.name.startswith('Mineral seam'))
r={'status':'PASS','three_lid_parented_pyramids':True,'pyramid_dimensions':sizes,'lid_dimensions':list(slab.dimensions),'lid_pivot':list(lid.location),'latch_pivot':list(latch.location),'packed_maps':[i.name for i in images],'no_other_country_ornaments':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r))
