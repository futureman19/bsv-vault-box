import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'czechia.blend'),use_scripts=False)
bpy.context.view_layer.update()
gems=[o for o in bpy.data.objects if o.name.startswith('Cut crystal /')]
def check():
 assert len(gems)==9
 assert all(o.parent and o.parent.name=='Lid_Hinge' for o in gems)
 assert all(len(o.data.polygons)==72 for o in gems)
 points=[o.matrix_world@v.co for o in gems for v in o.data.vertices]
 assert max(v.z for v in points)<2.65 and min(v.z for v in points)>=1.979
 assert max(abs(v.x) for v in points)<1.5 and max(abs(v.y) for v in points)<.9
 assert abs(bpy.data.objects['Lid / polished slab'].dimensions.x-3.72)<1e-5
check()
old=gems[0].parent;gems[0].parent=None
try:check();raise RuntimeError('negative control failed to reject')
except AssertionError:negative=True
gems[0].parent=old;check()
result={'status':'PASS','ornaments':len(gems),'facets_each':72,'lid_parentage':True,'ornament_bounds':True,'detached_ornament_rejected':negative,'negative_control':'post-implementation deliberate detached ornament; restored without saving'}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(result)
