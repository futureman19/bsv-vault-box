import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'cambodia.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
if '--negative' in sys.argv:bpy.data.objects['Baray / water'].parent=None
orn=[o for o in bpy.data.objects if o.name.startswith(('Baray /','Sanctuary /','Garden /'))]
assert len(orn)==18,len(orn)
assert all(o.parent==lid for o in orn),'Detached ornament rejected'
assert len([o for o in orn if o.name.startswith('Sanctuary / tier')])==3
assert len([o for o in orn if o.name.startswith('Sanctuary / pinnacle')])==5
pts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
assert 2.85<=max(p.z for p in pts)<=3.05
hits=[]
for x in [-.95,-.65,-.35]:
 for y in [-.5,0,.4]:
  hit,loc,n,i,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
  assert hit and obj.name=='Baray / water',(x,y,obj.name)
  hits.append([x,y,loc.z])
# Independently compare saved-source pivot transforms against the included mechanism.
pivots={n:list(bpy.data.objects[n].matrix_local) for n in ['Lid_Hinge','Latch_Pivot']}
pivots={n:[[float(x) for x in row] for row in matrix] for n,matrix in pivots.items()}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in pivots.items():
 assert max(abs(rows[i][j]-bpy.data.objects[n].matrix_local[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','ornaments':len(orn),'all_lid_owned':True,'water_surface_rays':hits,'summit_z':max(p.z for p in pts),'inherited_pivot_parity':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
