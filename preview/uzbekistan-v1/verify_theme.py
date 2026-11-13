import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'uzbekistan.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
petals=[o for o in bpy.data.objects if o.name.startswith('Rishtan / petal')]
if '--negative-detach' in sys.argv:petals[0].parent=None
assert len(petals)==8
orn=[o for o in bpy.data.objects if o.name.startswith('Rishtan /')]
assert all(o.parent==lid for o in orn),'Ornament detached from lid'
verts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
assert max(v.z for v in verts)<2.14 and min(v.z for v in verts)>=1.97
assert max((v.x*v.x+v.y*v.y)**.5 for v in verts)<.735
skins=[o for o in bpy.data.objects if o.name.startswith('Ceramic /') and ('front' in o.name or 'rear' in o.name or 'side' in o.name)]
assert len(skins)==4
bounds=[([min((o.matrix_world@Vector(v))[i] for v in o.bound_box) for i in range(3)],[max((o.matrix_world@Vector(v))[i] for v in o.bound_box) for i in range(3)]) for o in skins]
for i,a in enumerate(bounds):
 for b in bounds[i+1:]:assert not all(min(a[1][j],b[1][j])-max(a[0][j],b[0][j])>1e-5 for j in range(3)),'Overlapping skin volumes'
pivots={o.name:list(o.matrix_world.translation) for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,v in pivots.items():assert (bpy.data.objects[n].matrix_world.translation-Vector(v)).length<1e-6
out={'status':'PASS','petals':len(petals),'all_ornaments_lid_owned':True,'ornament_z':[min(v.z for v in verts),max(v.z for v in verts)],'ornament_radius_max':max((v.x*v.x+v.y*v.y)**.5 for v in verts),'skin_corner_nonoverlap':True,'baseline_pivots_unchanged':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS',json.dumps(out))
