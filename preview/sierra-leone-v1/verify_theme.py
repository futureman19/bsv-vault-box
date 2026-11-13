import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'sierra-leone.blend'),use_scripts=False)
bpy.context.view_layer.update()
def check():
 lid=bpy.data.objects['Lid_Hinge'];objs=list(bpy.data.objects)
 groups={k:[o for o in objs if o.name.startswith('Gola / '+k)] for k in ['trunk','buttress','branch','broadleaf cluster']}
 assert len(groups['trunk'])==3 and len(groups['broadleaf cluster'])>=30
 assert len(groups['branch'])>=9 and len(groups['buttress'])>=9
 for members in groups.values():
  for o in members:assert o.parent==lid,o.name
 foliage=groups['broadleaf cluster'];assert len({o.data.materials[0].name for o in foliage})>=3
 zs=[(o.matrix_world@v.co).z for o in foliage for v in o.data.vertices];assert max(zs)<=1.978+1.15
 assert all(o.dimensions.z<o.dimensions.x*.65 for o in foliage)
 assert len([o for o in objs if o.name.startswith('Bark relief')])>=30
 assert bpy.data.objects['Forest floor / island'].parent==lid
 # Roots actually contact the irregular island; evaluate underside rays.
 island=bpy.data.objects['Forest floor / island'];roots=[]
 for o in groups['trunk']:
  world=o.matrix_world@o.data.vertices[0].co
  hit,co,no,idx=island.ray_cast(island.matrix_world.inverted()@Vector((world.x,world.y,3)),Vector((0,0,-1)))
  assert hit
  surface=(island.matrix_world@co).z
  low=min((o.matrix_world@v.co).z for v in o.data.vertices)
  assert abs(low-surface)<.09,(o.name,low,surface)
  roots.append({'name':o.name,'root_z':low,'island_z':surface})
 return {'status':'PASS','groups':{k:len(v) for k,v in groups.items()},'max_canopy_z':max(zs),'roots':roots}
r=check()
o=bpy.data.objects['Gola / trunk 0'];p=o.parent;o.parent=None
try:check()
except AssertionError:r['detached_trunk_negative_control']='FAIL as expected'
else:raise AssertionError('negative control did not fail')
o.parent=p
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
