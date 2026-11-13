"""Independent saved-source brief gates. --negative removes lid ancestry in memory."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'bahrain.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
orn=[bpy.data.objects[n] for n in ['Oyster / lower radial valve','Oyster / raised radial valve','Pearl / central ivory']]
negative='--negative' in sys.argv
if negative:orn[0].parent=None
assert all(o.parent==lid for o in orn),'Ornament escaped lid hierarchy'
assert latch.parent==lid
bpy.context.view_layer.update()
verts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
bounds=[[min(v[i] for v in verts),max(v[i] for v in verts)] for i in range(3)]
assert bounds[0][1]-bounds[0][0]<=1.45 and bounds[1][1]-bounds[1][0]<=1.1 and bounds[2][1]-1.978<=.75,bounds
p=orn[2];assert all(abs(d-.38)<1e-5 for d in p.dimensions)
assert all(len(o.data.polygons)>1000 for o in orn[:2])
assert not any('Cedar' in o.name or 'Terrain' in o.name for o in bpy.data.objects)
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
assert all(o.dimensions.z<=.10001 for o in bpy.data.objects if o.name.startswith('Seam /'))
assert abs(lid.location.y-1.32)<1e-5 and abs(lid.location.z-1.668)<1e-5
images=[im for im in bpy.data.images if im.packed_file];assert len(images)==3
assert all(max(im.size)<=512 for im in images)
r={'status':'PASS','ornament_bounds_xyz':bounds,'ornament_meshes':[o.name for o in orn],'shell_polygon_counts':[len(o.data.polygons) for o in orn[:2]],'pearl_diameter':list(p.dimensions),'lid_dimensions':list(slab.dimensions),'lid_pivot':list(lid.location),'latch_pivot':list(latch.location),'packed_maps':[im.name for im in images],'ornaments_move_with_lid':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r))
