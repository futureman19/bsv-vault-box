import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.view_layer.update()
pivots={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'djibouti.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];terrain=[o for o in bpy.data.objects if o.name.startswith('Terrain /')]
if '--negative' in sys.argv: terrain[0].parent=None
assert len(terrain)==34
assert all(o.parent==lid for o in terrain),'detached terrain'
for n,m in pivots.items():
 assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-6
v=[o.matrix_world@v.co for o in terrain for v in o.data.vertices]
assert max(p.z for p in v)<1.978+.65
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
lake=bpy.data.objects['Terrain / Assal lake'];shelf=bpy.data.objects['Terrain / salt shelf']
assert all(p.normal.z>.99 for p in lake.data.polygons)
assert all(p.normal.z>.9 for p in shelf.data.polygons[96:192])
hits=[]
for x in [-.7,0,.7]:
 hit,loc,normal,idx,obj,_=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,0,3)),Vector((0,0,-1)))
 assert hit and obj==lake;hits.append(list(loc))
for o in bpy.data.objects:
 if o.name.startswith('Mineral seam'):assert o.dimensions.z<.12
images=[]
for i in bpy.data.images:
 if i.packed_file:assert max(i.size)<=1024;images.append(i.name)
assert len(images)>=4
result={'status':'PASS','terrain_meshes':len(terrain),'max_terrain_z':max(p.z for p in v),'lake_visible_rays':hits,'salt_top_normals_up':True,'pivots_equal_baseline':True,'slab_dimensions':list(slab.dimensions),'packed_images':images}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(result)
