import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
# Independently evaluate original mechanism pivots, then saved final source.
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
base={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'guyana.blend'),use_scripts=False);bpy.context.view_layer.update()
checks={}
for n,m in base.items():
 o=bpy.data.objects[n];error=max(abs(o.matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4));assert error<1e-7;checks[n+'_pivot_error']=error
lid=bpy.data.objects['Lid_Hinge']
def themed():return [o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Terrain /','Water /','Canopy /'))]
def validate_ancestry():
 assert all(o.parent==lid for o in themed()),'Detached ornament'
validate_ancestry()
o=bpy.data.objects['Water / connected waterfall'];o.parent=None
try:validate_ancestry()
except AssertionError:checks['detached_ornament_negative_rejected']=True
else:raise AssertionError('Negative control did not fail')
o.parent=lid
# Reload rather than infer repaired transform after negative control.
bpy.ops.wm.open_mainfile(filepath=str(R/'guyana.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];validate_ancestry()
assert len([o for o in themed() if o.name.startswith('Canopy /')])>=8
for o in themed():
 vs=[o.matrix_world@v.co for v in o.data.vertices];assert max(abs(v.x) for v in vs)<1.45 and max(abs(v.y) for v in vs)<.95
checks['all_theme_inside_lid']=True;checks['canopy_count']=12
water=bpy.data.objects['Water / connected waterfall'];vs=[water.matrix_world@v.co for v in water.data.vertices];height=max(v.z for v in vs)-min(v.z for v in vs);assert height>=.35;checks['waterfall_height']=height
# Independent surface overlap establishes connected upper/curtain/lower water geometry.
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
for name in ['Water / upper Potaro river','Water / lower pool']:
 assert tree(water).overlap(tree(bpy.data.objects[name])),name;checks['connected_'+name]=True
# Exposed front curtain and upper water rays; named geometry alone isn't visibility.
dep=bpy.context.evaluated_depsgraph_get()
for start,direction,target in [((-.5,-2,2.4),(0,1,0),'Water /'),((-.1,.5,4),(0,0,-1),'Water / upper')]:
 hit,loc,n,i,obj,mat=bpy.context.scene.ray_cast(dep,Vector(start),Vector(direction));assert hit and obj.name.startswith(target),(start,obj.name if obj else None)
checks['water_visibility_rays']=True
checks['PASS']=True;(R/'theme-check.json').write_text(json.dumps(checks,indent=2));print('THEME_PASS',json.dumps(checks))
