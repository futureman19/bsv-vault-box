import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'brunei.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
def check():
 ornaments=[o for o in bpy.data.objects if o.name.startswith('Tenunan diamond')]
 assert len(ornaments)==15
 for o in ornaments:
  assert o.parent==lid, o.name
  v=[o.matrix_world@v.co for v in o.data.vertices]
  assert 1.972<min(p.z for p in v)<1.985 and max(p.z for p in v)<2.0
  x=sum(p.x for p in v)/len(v) # closed duplicate first vertex biases mean, use bounds centre
  x=(max(p.x for p in v)+min(p.x for p in v))/2;y=(max(p.y for p in v)+min(p.y for p in v))/2
  hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,2.5)),Vector((0,0,-1)))
  assert hit and obj.name=='Lid / polished slab',(o.name,obj.name)
 return len(ornaments)
n=check();o=next(o for o in bpy.data.objects if o.name.startswith('Tenunan diamond'));o.parent=None
try:check()
except AssertionError as e:negative='PASS: detached ornament rejected: '+str(e)
else:raise AssertionError('Negative control not rejected')
o.parent=lid
r={'status':'PASS','diamond_count':n,'apertures_reach_solid_lid':True,'all_lid_owned':True,'height_envelope':[1.972,2.0],'negative_control':negative}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
