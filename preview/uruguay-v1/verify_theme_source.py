import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'uruguay.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
terrain=[o for o in bpy.data.objects if o.name.startswith('Terrain /')]
def owned():return all(o.parent==lid for o in terrain)
assert len(terrain)==21 and owned()
# Real detached-ornament negative control, restored before subsequent checks.
o=terrain[0];o.parent=None;assert not owned();o.parent=lid
negative={'detached_lid_ornament_rejected':True}
bpy.context.view_layer.update()
stream=bpy.data.objects['Terrain / Yerbal stream'];banks=[o for o in terrain if 'bank' in o.name]
def bvh(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();v=[o.matrix_world@v.co for v in m.vertices];t=BVHTree.FromPolygons(v,[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
water=bvh(stream);others=[bvh(o) for o in terrain if o!=stream];rays=[]
for i in range(31):
 y=-.85+1.7*i/30;x=.26*math.sin(3*y);origin=Vector((x,y,3));direction=Vector((0,0,-1));hit=water.ray_cast(origin,direction);assert hit[0] is not None
 heights=[t.ray_cast(origin,direction)[0] for t in others];assert all(p is None or p.z<hit[0].z for p in heights)
 rays.append([x,y,hit[0].z])
verts=[o.matrix_world@v.co for o in banks for v in o.data.vertices]
assert min(v.x for v in verts)>=-1.51 and max(v.x for v in verts)<=1.51
assert max(v.z for v in verts)>2.30 and max(v.z for v in verts)<2.45
assert min(v.z for v in verts)<=1.979,'Banks must meet lid surface'
# Compare fully evaluated inherited pivot matrices, not unlinked appended data.
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(pivots[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in pivots for i in range(4) for j in range(4));assert error<1e-7
result={'status':'PASS','terrain_meshes':len(terrain),'stream_centerline_visible_rays':rays,'terrain_height_max':max(v.z for v in verts),'pivot_matrix_max_error':error,'negative_controls':negative,'scope':'sampled vertical channel visibility, not camera occlusion or literal geography'}
(R/'theme-source-check.json').write_text(json.dumps(result,indent=2));print('THEME SOURCE PASS',json.dumps(result))
