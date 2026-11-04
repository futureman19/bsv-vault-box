"""Independent saved-source theme geometry and inherited pivot assertions."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'pacific-ocean.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];ring=bpy.data.objects['Atoll / coral sand ring'];water=bpy.data.objects['Atoll / lagoon'];volcano=bpy.data.objects['Seamount / basalt crater']
def check():
 for o in [ring,water,volcano]:assert o.parent==lid,('Detached ornament',o.name)
 # Radial containment checked against each irregular inner edge, not bbox.
 inner=[ring.matrix_world@v.co for v in ring.data.vertices[288:384]]
 def inside(p):
  hit=False
  for a,b in zip(inner,inner[1:]+inner[:1]):
   if (a.y>p.y)!=(b.y>p.y) and p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x:hit=not hit
  return hit
 assert all(inside(water.matrix_world@v.co) for v in water.data.vertices),'Lagoon escaped ring'
 dep=bpy.context.evaluated_depsgraph_get()
 def ray(x,y):return bpy.context.scene.ray_cast(dep,Vector((x,y,4)),Vector((0,0,-1)))
 h=ray(-.3,0);assert h[0] and h[4]==water,'Lagoon aperture occluded'
 for i in range(32):
  t=i*math.tau/32;h=ray(-.3+.76*math.cos(t),.55*math.sin(t));assert h[0] and h[4]==ring,('Ring discontinuity',i)
 assert max((volcano.matrix_world@v.co).z for v in volcano.data.vertices)<=2.458
 assert min((volcano.matrix_world@v.co).x for v in volcano.data.vertices)>.70
check();neg=[]
old=water.parent;water.parent=None
try:check()
except AssertionError as e:neg.append(str(e))
else:raise AssertionError('Negative detached-lagoon control incorrectly passed')
water.parent=old;bpy.context.view_layer.update()
old=water.location.copy();water.location.x+=1.5;bpy.context.view_layer.update()
try:check()
except AssertionError as e:neg.append(str(e))
else:raise AssertionError('Negative escaped-lagoon control incorrectly passed')
water.location=old;bpy.context.view_layer.update();check()
r={'status':'PASS','same_mechanism_pivots':True,'lagoon_boundary_vertices_contained':len(water.data.vertices),'open_center_water_ray':True,'ring_rays':32,'all_ornaments_lid_owned':True,'negative_controls_rejected':neg,'limitations':'Source rays and containment, not photorealism or hydrology.'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r))
