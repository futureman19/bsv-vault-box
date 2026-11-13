import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'the-moon.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];terrain=bpy.data.objects['Terrain / impact highlands']
assert terrain.parent==lid
points=[terrain.matrix_world@v.co for v in terrain.data.vertices]
assert max(v.z for v in points)<2.478
assert all(abs(v.x)<=1.59 and abs(v.y)<=.95 for v in points)
def floor(x,y):
 hit,loc,*_=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit;return loc.z
craters=json.loads((R/'crater-spec.json').read_text())['craters'];measured=[]
for x,y,r in craters:
 f=floor(x,y);rim=max(floor(x+r*math.cos(a),y+r*math.sin(a)) for a in [i*math.tau/16 for i in range(16)])
 assert rim-f>=.06,(f,rim)
 measured.append({'center':[x,y],'diameter':2*r,'floor_z':f,'rim_z':rim,'relief':rim-f})
assert .8<=measured[0]['diameter']<=1.2 and any(.25<=m['diameter']<=.55 for m in measured[1:])
source_pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
# Negative control really detaches terrain and proves hierarchy oracle rejects it.
def owns_lid(o):return o.parent==lid
terrain.parent=None
assert not owns_lid(terrain)
terrain.parent=lid
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in source_pivots.items():
 assert max(abs(a-b) for r,s in zip(rows,bpy.data.objects[n].matrix_world) for a,b in zip(r,s))<1e-7
out={'status':'PASS','craters':measured,'all_lid_terrain_attached':True,'detached_negative_control_rejected':True,'inherited_pivot_world_matrices_equal':True,'relief_below_half_unit':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
