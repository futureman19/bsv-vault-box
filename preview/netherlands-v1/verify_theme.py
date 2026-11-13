import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'netherlands.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')]
fields=[o for o in meshes if o.name.startswith('Polder / field')];sails=[o for o in meshes if o.name.startswith('Mill / sail ') and not o.name.startswith('Mill / sail rib')]
assert len(fields)==8 and len(sails)==4
ornaments=[o for o in meshes if o.name.startswith(('Polder','Mill'))]
assert all(o.parent==lid for o in ornaments)
assert not any(any(s in o.name for s in ['Cedar','Granite','moss','Iceland']) for o in meshes)
def bounds(o):
 v=[o.matrix_world@Vector(p) for p in o.bound_box];return [min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]
assert all(bounds(o)[1][2]<=2.258 for o in ornaments if o.name.startswith('Polder'))
assert max(bounds(o)[1][2] for o in ornaments)<3.078
assert bounds(bpy.data.objects['Mill / tower'])[0][0]>0 and bounds(bpy.data.objects['Mill / tower'])[0][1]>0
# Downward source rays independently establish visible channels and raised fields.
def hit(x,y):
 ok,p,n,i,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3.5)),Vector((0,0,-1)));assert ok;return o.name,p.z
water_points=[(-.68,0),(0,0),(.68,0),(-.68,-.36),(-.68,.36)]
for x,y in water_points:assert hit(x,y)[0]=='Polder / water bed',(x,y,hit(x,y))
for o in fields:
 p=o.matrix_world.translation
 # Offset from the rear/right mill footprint, keeping the ray within each parcel.
 assert hit(p.x+.20,p.y+.20)[0]==o.name,(o.name,hit(p.x+.20,p.y+.20))
# Exact independent saved-baseline pivot matrix comparison.
actual={o.name:[list(r) for r in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,rows in actual.items():assert max(abs(rows[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
result={'status':'PASS','fields':len(fields),'sails':len(sails),'lid_owned_ornaments':len(ornaments),'perpendicular_water_ray_hits':len(water_points),'inherited_pivot_matrices_match':True,'no_inherited_country_ornaments':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
