"""Independent saved-source visual contract. --negative removes a ridge in memory."""
import bpy,json,sys,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
expected={n:tuple(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'namibia.blend'),use_scripts=False)
if '--negative' in sys.argv:bpy.data.objects.remove(bpy.data.objects['Dune ridge / 3'],do_unlink=True)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert latch.parent==lid
for n,loc in expected.items():assert max(abs(a-b) for a,b in zip(bpy.data.objects[n].location,loc))<1e-7,(n,loc)
ridges=[o for o in bpy.data.objects if o.name.startswith('Dune ridge /')]
assert len(ridges)==3,('Expected 3 real dune ridges',len(ridges))
measure=[]
for o in ridges:
 assert o.parent==lid and len(o.data.polygons)>=1000
 points=[o.matrix_world@v.co for v in o.data.vertices];zs=[p.z for p in points];h=max(zs)-min(zs)
 assert .15<h<.65,(o.name,h)
 # Crest cannot be a straight line: for each longitudinal row, find highest vertex.
 ys=[max(points[i:i+21],key=lambda p:p.z).y for i in range(21,len(points)-21,21)]
 assert max(ys)-min(ys)>.10
 measure.append({'name':o.name,'relief_height':h,'crest_y_span':max(ys)-min(ys)})
pan=bpy.data.objects['Playa / ivory basin'];assert pan.parent==lid and len(pan.data.polygons)==80
from mathutils import Vector
cam=bpy.context.scene.camera;visible=0
for dx,dy in [(0,0),(-.25,0),(.25,0),(0,-.10),(0,.10),(-.2,-.08),(.2,.08)]:
 target=Vector((.93+dx,-.65+dy,1.995));direction=(target-cam.location).normalized()
 hit,loc,normal,index,obj,matrix=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),cam.location,direction)
 visible+=bool(hit and obj==pan)
assert visible>=5,('Playa is occluded from source hero camera',visible)
assert all(o.dimensions.z<=.1 for o in bpy.data.objects if o.name.startswith('Mineral seam'))
slab=bpy.data.objects['Lid / polished slab'];assert max(abs(a-b) for a,b in zip(slab.dimensions,(3.72,2.38,.30)))<1e-5
assert not any('Cedar' in o.name or 'moss' in o.name.lower() or 'glacier' in o.name.lower() for o in bpy.data.objects)
packed=[i for i in bpy.data.images if i.packed_file];assert len(packed)==3
assert all(max(i.size)<=1024 for i in packed)
out={'status':'PASS','pivots_unchanged':expected,'lid_dimensions':list(slab.dimensions),'ridges':measure,'pan_faces':80,'pan_visible_rays':visible,'packed_maps':[i.name for i in packed],'negative_control':False}
(R/'theme-source-check.json').write_text(json.dumps(out,indent=2));print('THEME SOURCE PASS',json.dumps(out))
