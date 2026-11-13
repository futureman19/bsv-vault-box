import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'finland.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Lake /','Island /'))]
if '--negative' in sys.argv:ornaments[-1].parent=None
assert len(ornaments)==4
assert all(o.parent==lid for o in ornaments),'Ornament detached from lid'
assert not any(o.name.startswith('Cedar tree') for o in bpy.data.objects)
for o in ornaments:
 v=[o.matrix_world@x.co for x in o.data.vertices]
 assert max(abs(x.x) for x in v)<1.48 and max(abs(x.y) for x in v)<.85
 assert min(x.z for x in v)>=1.975-1e-5 and max(x.z for x in v)<=2.18
lake=bpy.data.objects['Lake / enamel basin']; islands=[o for o in ornaments if o!=lake]
def hit(x,y):
 ok,loc,n,idx,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)));assert ok;return obj.name
water=[hit(x,y) for x,y in [(-.35,-.1),(.34,-.1),(0,-.5),(.95,.1),(-1,.1)]]
assert all(x==lake.name for x in water),water
for o in islands:assert hit(o.data.vertices[0].co.x*.0+sum(v.co.x for v in o.data.vertices)/len(o.data.vertices),sum(v.co.y for v in o.data.vertices)/len(o.data.vertices))==o.name
current={n:list(bpy.data.objects[n].matrix_world.translation) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
assert all(max(abs(a-b) for a,b in zip(current[n],bpy.data.objects[n].matrix_world.translation))<1e-6 for n in current)
r={'status':'PASS','ornaments':4,'islands':3,'water_visibility_rays':water,'original_pivots':current,'negative_control':'--negative detaches one island and must fail'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',r)
