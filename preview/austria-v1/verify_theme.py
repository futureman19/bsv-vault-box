import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'austria.blend'),use_scripts=False)
bpy.context.view_layer.update()
o=bpy.data.objects['Terrain / Alpine crown'];lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
if '--negative' in sys.argv:o.parent=None
assert o.parent==lid,'Crown must travel with the lid'
verts=[o.matrix_world@v.co for v in o.data.vertices];z=[v.z for v in verts]
assert min(z)>=1.969 and min(z)<1.978 and 2.6<max(z)<2.95
assert len(o.data.materials)==3
counts={m.name:sum(p.material_index==i for p in o.data.polygons) for i,m in enumerate(o.data.materials)}
assert all(n>15 for n in counts.values())
assert len([x for x in bpy.data.objects if x.name.startswith('Adnet /')])==4
# Actual downward samples through each promised summit; no illustrative substitute.
rays=[]
for x,y in [(-.65,.12),(.15,.26),(.86,.04)]:
 hit,loc,normal,index,obj,matrix=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
 assert hit and obj==o and loc.z>2.35
 rays.append(list(loc))
# Compare evaluated source pivots independently with frozen mechanical source.
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(bpy.data.objects[n].matrix_world[i][j]-pivots[n][i][j]) for n in pivots for i in range(4) for j in range(4));assert err<1e-7
result={'status':'PASS','crown_z_bounds':[min(z),max(z)],'material_polygon_counts':counts,'summit_ray_hits':rays,'pivot_matrix_max_error':err,'direct_lid_parent':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
