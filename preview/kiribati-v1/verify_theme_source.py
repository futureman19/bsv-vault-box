"""Independent saved-source theme/attachment/pivot assertions, with negative controls."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
names=['Lid_Hinge','Latch_Pivot'];baseline={n:[list(row) for row in bpy.data.objects[n].matrix_local] for n in names}
bpy.ops.wm.open_mainfile(filepath=str(R/'kiribati.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];errors=[]
for n in names:
 actual=bpy.data.objects[n].matrix_local;error=max(abs(actual[i][j]-baseline[n][i][j]) for i in range(4) for j in range(4));errors.append(error);assert error<1e-7
assert latch.parent==lid
objects=[o for o in bpy.data.objects if o.name.startswith(('Atoll /','Atoll vegetation /','Lagoon /'))]
def owned():assert objects and all(o.parent==lid for o in objects),'detached terrain'
owned();target=objects[0];mw=target.matrix_world.copy();target.parent=None
try:owned()
except AssertionError:negative=True
else:raise AssertionError('Ancestry negative control incorrectly accepted')
target.parent=lid;target.matrix_world=mw;bpy.context.view_layer.update();owned()
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();result=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[tuple(p.vertices) for p in me.polygons]);ev.to_mesh_clear();return result
rim=bpy.data.objects['Atoll / continuous C rim'];bvh=tree(rim)
rays=[]
for angle in [0,45,90,135,180,270,315]:
 a=math.radians(angle);x,y=1.23*math.cos(a),.625*math.sin(a);hit=bvh.ray_cast(Vector((x,y,3)),Vector((0,0,-1)))[0];assert hit is not None and 2.06<hit.z<2.20;rays.append({'angle':angle,'z':hit.z})
for t in [.3,.5,.7,1]:
 a=math.radians(225);assert bvh.ray_cast(Vector((1.4*t*math.cos(a),.79*t*math.sin(a),3)),Vector((0,0,-1)))[0] is None,'sand blocks passage'
basin=tree(bpy.data.objects['Lagoon / inset basin']);center=basin.ray_cast(Vector((0,0,3)),Vector((0,0,-1)))[0];assert center and abs(center.z-2)<1e-5
plants=[]
for o in objects:
 if not o.name.startswith('Atoll vegetation'):continue
 coords=[o.matrix_world@v.co for v in o.data.vertices];bottom=min(v.z for v in coords);top=max(v.z for v in coords);xy=o.matrix_world.translation
 hit=bvh.ray_cast(Vector((xy.x,xy.y,3)),Vector((0,0,-1)))[0];assert hit is not None and bottom<hit.z<top,(o.name,bottom,hit,top);plants.append({'name':o.name,'bottom':bottom,'rim_z':hit.z,'top':top})
assert len(plants)==18
allz=[(o.matrix_world@v.co).z for o in objects for v in o.data.vertices];assert min(allz)>1.95 and max(allz)<2.30
panels=[o for o in bpy.data.objects if o.name.startswith('Pandanus /')];assert len(panels)==4
result={'status':'PASS','pivot_matrix_max_errors':errors,'theme_lid_meshes':len(objects),'detached_ornament_negative_rejected':negative,'rim_ray_samples':rays,'gap_rays_clear':4,'basin_center_z':center.z,'root_attachment_rays':plants,'ornament_z_range':[min(allz),max(allz)],'woven_panels':len(panels),'limitations':'sampled surface/root checks, not botanical or geographic accuracy'}
(R/'theme-source-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
