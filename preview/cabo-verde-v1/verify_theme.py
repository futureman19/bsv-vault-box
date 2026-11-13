"""Independent reopened-source shape/material contract; negative controls are separate."""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'cabo-verde.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];bpy.context.view_layer.update()
def world(o):return [o.matrix_world@v.co for v in o.data.vertices]
def ray(o,x,y):
 pts=world(o);tree=BVHTree.FromPolygons(pts,[list(p.vertices) for p in o.data.polygons]);return tree.ray_cast(Vector((x,y,4)),Vector((0,0,-1)))[0]
def check():
 cone=bpy.data.objects['Fogo / cratered cone'];ridge=bpy.data.objects['Caldera / open east horseshoe']
 assert cone.parent==lid and ridge.parent==lid
 assert all(p.normal.z>0 for p in ridge.data.polygons),'ridge normals must face upward'
 pts=world(cone);zmax=max(v.z for v in pts);center=ray(cone,-.18,.02);rim=ray(cone,-.18+.245,.02)
 assert center is not None and rim is not None and rim.z-center.z>.25,'crater must be a depressed bowl'
 assert 2.53<zmax<2.84,'cone height'
 assert ray(ridge,1.2,0) is None,'east caldera opening required'
 assert ray(ridge,-1.2,0) is not None,'west caldera wall required'
 assert max(v.x for v in world(ridge))-min(v.x for v in world(ridge))<2.9
 assert max(v.y for v in world(ridge))-min(v.y for v in world(ridge))<1.65
 assert abs(bpy.data.objects['Scoria / front'].dimensions.x-3.72)<1e-5
 assert abs(bpy.data.objects['Lid / polished slab'].dimensions.y-2.38)<1e-5
 assert latch.parent==lid
 # Exact mechanism matrices compared against frozen source, below.
 for o in bpy.data.objects:
  if o.name.startswith(('Caldera /','Fogo /','Cultivation /')):assert o.parent==lid,o.name
  if o.name.startswith('Atlantic seam'):assert o.dimensions.z<=.10
 stone=bpy.data.materials['Fogo / porous volcanic stone'];p=stone.node_tree.nodes.get('Principled BSDF')
 assert p.inputs['Base Color'].is_linked and p.inputs['Roughness'].is_linked and p.inputs['Normal'].is_linked
 images=[i for i in bpy.data.images if i.packed_file];assert len(images)==3
 maps=[]
 for i in images:
  assert max(i.size)<=512
  values=list(i.pixels)[::4];rng=max(values)-min(values);assert rng>.001
  maps.append({'name':i.name,'size':list(i.size),'red_range_linear':rng})
 return {'crater_depth':rim.z-center.z,'cone_max_z':zmax,'east_gap':True,'west_ridge':True,'maps':maps,'terrain_parentage':True,'seam_height_max':max(o.dimensions.z for o in bpy.data.objects if o.name.startswith('Atlantic seam'))}
r=check()
# Post-implementation negative: destroy crater depression and require rejection.
cone=bpy.data.objects['Fogo / cratered cone'];saved=[v.co.copy() for v in cone.data.vertices]
for v in cone.data.vertices:v.co.z=2.73
try:
 check();raise RuntimeError('Negative crater control was accepted')
except AssertionError as e:r['negative_control']={'mutation':'flattened every cone vertex to summit height in memory only','rejected':True,'message':str(e)}
for v,c in zip(cone.data.vertices,saved):v.co=c
# Load immutable trimmed mechanism only after collecting the candidate values.
actual={n:{'location':list(bpy.data.objects[n].location),'rotation':list(bpy.data.objects[n].rotation_euler)} for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
expected={n:{'location':list(bpy.data.objects[n].location),'rotation':list(bpy.data.objects[n].rotation_euler)} for n in actual}
assert actual==expected,(actual,expected);r['exact_pivots']=actual;r['status']='PASS'
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r))
