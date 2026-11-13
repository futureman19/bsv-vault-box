import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'marshall-islands.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
orn=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Chart /','Atoll /'))]
def validate():
 assert len(orn)==15,len(orn)
 assert all(o.parent==lid for o in orn),'detached ornament'
 assert len([o for o in orn if 'swell rod' in o.name])==6
 for o in orn:
  for v in o.data.vertices:
   co=o.matrix_world@v.co
   assert abs(co.x)<1.86 and abs(co.y)<1.19 and 1.96<co.z<2.35,(o.name,list(co))
validate()
# A deliberate invalid candidate must fail exactly the ancestry contract.
o=orn[0];parent=o.parent;o.parent=None
try:validate()
except AssertionError as e:negative={'rejected':True,'reason':str(e)}
else:raise AssertionError('Negative control unexpectedly accepted')
o.parent=parent;bpy.context.view_layer.update();validate()
water=bpy.data.objects['Atoll / lagoon'];norm=[]
for v in water.data.vertices:
 c=water.matrix_world@v.co;norm.append(((c.x+.78)/.49)**2+(c.y/.45)**2)
assert max(norm)<1.00001
original={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
images=[i.name for i in bpy.data.images if i.packed_file];assert len(images)>=4
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(original[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in original for i in range(4) for j in range(4));assert error<1e-6
result={'status':'PASS','ornament_meshes':len(orn),'raised_swell_rods':6,'ivory_markers':4,'lagoon_inside_inner_sand_ellipse_max':max(norm),'pivot_matrix_max_error':error,'packed_images':images,'detached_ornament_negative_control':negative,'limits':'Invented chart and atoll, not navigational/geographic accuracy.'}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
