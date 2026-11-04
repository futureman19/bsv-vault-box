import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'guinea.blend'),use_scripts=False)
bpy.context.view_layer.update()
objects=bpy.data.objects;ridge=objects['Terrain / Nimba ridge'];lid=objects['Lid_Hinge'];latch=objects['Latch_Pivot']
assert ridge.parent==lid and latch.parent==lid
v=[ridge.matrix_world@p.co for p in ridge.data.vertices]
dims=[max(p[i] for p in v)-min(p[i] for p in v) for i in range(3)]
assert 1.6<dims[0]<2.8 and .5<dims[1]<1.4 and .35<dims[2]<.8,dims
# Distinct peak neighborhoods along the long axis.
peaks=[]
for a,b in [(-1.1,-.45),(-.3,.4),(.5,1.1)]:
 peaks.append(max(p.z for p in v if a<p.x<b))
assert len(set(round(z,2) for z in peaks))==3,peaks
clusters=[o for o in objects if o.name.startswith('Terrain / forest cluster')]
assert len(clusters)==42 and all(o.parent==lid for o in clusters)
assert not any('Cedar' in o.name or 'glacier' in o.name.lower() for o in objects)
seams=[o for o in objects if o.name.startswith('Mineral seam')];assert seams and all(o.dimensions.z<.12 for o in seams)
slab=objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.001 and abs(slab.dimensions.y-2.38)<.001
assert abs(lid.location.y-1.32)<.001 and abs(lid.location.z-1.668)<.001
maps=[]
for im in bpy.data.images:
 if im.packed_file:
  assert max(im.size)<=1024
  maps.append({'name':im.name,'size':list(im.size)})
assert len(maps)>=3
result={'status':'PASS','ridge_dimensions':dims,'peak_heights':peaks,'forest_clusters':len(clusters),'all_terrain_on_lid':True,'seam_max_height':max(o.dimensions.z for o in seams),'packed_maps':maps,'lid_pivot':list(lid.location),'latch_pivot':list(latch.location)}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
