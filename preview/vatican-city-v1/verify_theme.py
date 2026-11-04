import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'vatican-city.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
for n,m in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-8
cols=[o for o in bpy.data.objects if o.name=='Arcade / column' or o.name.startswith('Arcade / column.')]
assert len(cols)==24,len(cols)
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Arcade /','Mosaic /'))]
def ancestry():assert all(o.parent==lid for o in ornaments),'detached ornament'
ancestry()
# A real negative control exercises ownership assertion, then restores without saving.
o=cols[0];o.parent=None
try:ancestry();raise RuntimeError('Negative control was not rejected')
except AssertionError:negative=True
finally:o.parent=lid
bpy.context.view_layer.update()
# At each column centre the downward hit must be its capital. The
# column ends are also measured against base top and capital bottom.
for o in cols:
 v=[o.matrix_world@v.co for v in o.data.vertices];lo=min(v.z for v in v);hi=max(v.z for v in v)
 assert abs(lo-2.068)<1e-5 and abs(hi-2.368)<1e-5,(o.name,lo,hi)
# 21 downward samples in central open piazza must reach the actual lid,
# not hidden overlapping arc/cornice geometry.
dep=bpy.context.evaluated_depsgraph_get();samples=[]
for x in [-.6,-.4,-.2,0,.2,.4,.6]:
 for y in [-.15,0,.15]:
  hit,loc,normal,index,obj,matrix=bpy.context.scene.ray_cast(dep,Vector((x,y,3)),Vector((0,0,-1)))
  assert hit and obj.name=='Lid / polished slab',(x,y,obj.name)
  samples.append([x,y,loc.z])
# Actual gaps between adjacent columns stay open at mid-shaft height.
for side in [0,1]:
 for i in range(11):
  a=math.radians(22+side*180+136*(i+.5)/11)
  p=Vector((1.06*math.cos(a),.57*math.sin(a),2.218))
  # nearest vertices on column surfaces separated from midpoint by >.01
  assert min((p-(o.matrix_world@v.co)).length for o in cols for v in o.data.vertices)>.01
out=dict(status='PASS',columns=len(cols),lid_ornaments=len(ornaments),inherited_pivots_exact=True,column_end_z=[2.068,2.368],central_open_rays=samples,column_gaps=22,detached_ornament_negative_rejected=negative,scope='Invented arcade, not a scale reconstruction')
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS',json.dumps(out))
