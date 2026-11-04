import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'nauru.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];pinnacles=[o for o in bpy.data.objects if o.name.startswith('Pinnacle /')]
negative='--negative-detached' in sys.argv
if negative:pinnacles[0].parent=None
assert len(pinnacles)>=7
for o in pinnacles:assert o.parent==lid,('Detached pinnacle',o.name)
def verts(o):return [o.matrix_world@v.co for v in o.data.vertices]
heights=[max(v.z for v in verts(o))-2.10 for o in pinnacles]
assert min(heights)>=.20 and max(heights)<=.65 and max(heights)-min(heights)>.3,heights
terrace=bpy.data.objects['Terrain / basin terrace'];lagoon=bpy.data.objects['Terrain / inland lagoon']
assert terrace.parent==lagoon.parent==lid
assert all(p.normal.z>0 for p in terrace.data.polygons[:96]), 'Terrace upper faces must face upward'
# Ray onto terrace at each pillar root: actual base rings must reach surface.
dep=bpy.context.evaluated_depsgraph_get();ev=terrace.evaluated_get(dep);root_checks=[]
for o in pinnacles:
 v=verts(o);x=sum(q.x for q in v[:9])/9;y=sum(q.y for q in v[:9])/9
 local=terrace.matrix_world.inverted()@Vector((x,y,3));hit,loc,normal,face=ev.ray_cast(local,Vector((0,0,-1)))
 assert hit and min(q.z for q in v)<(terrace.matrix_world@loc).z
 root_checks.append({'name':o.name,'root_surface_z':(terrace.matrix_world@loc).z})
# Polygon containment, all lagoon vertices within terrace outer boundary.
outer=[(v.x,v.y) for v in verts(terrace)[96:144]]
def inside(x,y):
 c=False
 for i,(ax,ay) in enumerate(outer):
  bx,by=outer[(i+1)%len(outer)]
  if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:c=not c
 return c
assert all(inside(v.x,v.y) for v in verts(lagoon))
water=verts(lagoon);assert max(v.x for v in water)-min(v.x for v in water)>.65 and max(v.y for v in water)-min(v.y for v in water)>.4
# Verify lagoon center visible from source camera using actual scene ray.
a=bpy.context.scene.camera.location;b=Vector((-.35,-.20,2.045));hit,loc,n,i,o,mat=bpy.context.scene.ray_cast(dep,a,(b-a).normalized());assert hit and o==lagoon,('Basin center occluded',o.name if o else None)
assert len([i for i in bpy.data.images if i.packed_file])>=3
out={'status':'PASS','pinnacles':len(pinnacles),'heights':heights,'roots':root_checks,'lagoon_contained':True,'lagoon_center_visible_from_source_camera':True,'all_ornaments_lid_owned':all(o.parent==lid for o in bpy.data.objects if o.name.startswith(('Terrain /','Pinnacle /')))}
assert out['all_ornaments_lid_owned'];(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
