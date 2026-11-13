import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mongolia.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
orn=[o for o in bpy.data.objects if o.name.startswith(('Ger /','Steppe /'))]
assert len(orn)==20,len(orn)
assert all(o.parent==lid for o in orn)
assert len([o for o in orn if o.name.startswith('Ger / roof cord')])==12
assert len([o for o in orn if o.name.startswith('Ger / rope band')])==2
terrain=bpy.data.objects['Steppe / rolling oval'];coords=[terrain.matrix_world@v.co for v in terrain.data.vertices]
assert abs(min(v.z for v in coords)-1.97)<1e-5
assert 2.02<max(v.z for v in coords)<2.16
# Ray from the ger wall footprint down to the actual terrain, not a bounds proxy.
roots=[]
for a in [i*math.tau/12 for i in range(12)]:
 x=.55+.39*math.cos(a);y=.25+.39*math.sin(a)
 hit,loc,normal,face=terrain.ray_cast(terrain.matrix_world.inverted()@Vector((x,y,2.3)),Vector((0,0,-1)))
 assert hit and abs((terrain.matrix_world@loc).z-2.10)<.018,(x,y,hit,loc)
 roots.append(float((terrain.matrix_world@loc).z))
wall=bpy.data.objects['Ger / felt wall'];assert (wall.matrix_world.translation-Vector((.55,.25,2.25))).length<1e-5
assert not any(o.name.startswith(('Cedar','Terrain / moss')) for o in bpy.data.objects)
# Negative control: the same ancestry gate must reject a detached roof.
roof=bpy.data.objects['Ger / peaked felt roof'];roof.parent=None
try:
 assert all(o.parent==lid for o in orn)
except AssertionError:negative=True
else:raise AssertionError('detached roof not rejected')
# Compare against separately opened baseline after capturing evaluated pivot matrices.
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','ornament_meshes':len(orn),'roof_cords':12,'rope_bands':2,'ger_root_terrain_z':roots,'all_ornaments_lid_owned':True,'detached_roof_negative_rejected':negative,'baseline_pivots_identical':True,'relief_height_range':[min(v.z for v in coords),max(v.z for v in coords)]}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
