import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
anchors={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'seychelles.blend'),use_scripts=False)
for n,v in anchors.items():assert max(abs(a-b) for a,b in zip(bpy.data.objects[n].location,v))<1e-7
lid=bpy.data.objects['Lid_Hinge'];bpy.context.view_layer.update()
terrain=[o for o in bpy.data.objects if o.name.startswith('Terrain /')]
assert len(terrain)==5 and all(o.parent==lid for o in terrain)
rocks=[o for o in terrain if 'boulder' in o.name];assert len(rocks)==3
assert not any('Cedar' in o.name or 'Finger' in o.name for o in bpy.data.objects)
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
assert all(max((o.matrix_world@v.co).z for v in o.data.vertices)-1.978<=.85 for o in rocks)
# Every lagoon boundary vertex must lie inside the actual authored sand polygon.
sand=bpy.data.objects['Terrain / sand crescent'];water=bpy.data.objects['Terrain / lagoon inlay']
poly=[sand.matrix_world@v.co for v in list(sand.data.vertices)[1:]]
def inside(p):
 odd=False;j=len(poly)-1
 for i in range(len(poly)):
  a,b=poly[i],poly[j]
  if (a.y>p.y)!=(b.y>p.y) and p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x:odd=not odd
  j=i
 return odd
outside=[i for i,v in enumerate(water.data.vertices) if not inside(water.matrix_world@v.co)]
result={'status':'FAIL' if outside else 'PASS','terrain_meshes':len(terrain),'boulders':len(rocks),'all_terrain_lid_parented':True,'preserved_pivots':anchors,'slab_dimensions':list(slab.dimensions),'lagoon_outside_sand_vertices':outside,'rock_max_world_z':max((o.matrix_world@v.co).z for o in rocks for v in o.data.vertices),'seam_max_height':max(o.dimensions.z for o in bpy.data.objects if o.name.startswith('Mineral seam'))}
assert result['seam_max_height']<.12
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not outside,'Lagoon protrudes beyond sand boundary'
