"""Independent saved-source feature gates and deliberately broken negative controls."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'botswana.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
channels=[o for o in bpy.data.objects if o.name.startswith('Delta / channel')]
def contract():
 assert len(channels)==5
 assert all(o.parent==lid for o in bpy.data.objects if o.name.startswith('Delta /'))
 assert all(p.normal.z>.99 for o in channels for p in o.data.polygons),'water must face upward'
 assert all(abs(o.location[i]-v)<1e-5 for o,xyz in [(lid,(0,1.32,1.668))] for i,v in enumerate(xyz)),'pivot drift'
 assert latch.parent==lid
 assert len([o for o in bpy.data.objects if o.name.startswith('Coil /')])==96
 assert not [o.name for o in bpy.data.objects if any(w in o.name for w in ['Cedar','Moss','Granite'])]
 slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.001 and abs(slab.dimensions.y-2.38)<.001
 for o in bpy.data.objects:
  if o.name.startswith('Delta /'):
   assert max((o.matrix_world@v.co).z for v in o.data.vertices)<2.358
 # Channel graph: each secondary ribbon has its first centre at an existing primary vertex pair.
 def centre(o,i):return o.matrix_world@((o.data.vertices[2*i].co+o.data.vertices[2*i+1].co)/2)
 for k in range(1,len(channels)):
  assert min((centre(channels[k],0)-centre(channels[j],i)).length for j in range(k) for i in range(len(channels[j].data.vertices)//2))<1e-5
 return True
bpy.context.view_layer.update();contract()
negative=[]
old=channels[0].parent;channels[0].parent=None
try:contract()
except AssertionError:negative.append('detached channel rejected')
else:raise AssertionError('negative hierarchy control accepted')
channels[0].parent=old
lid.location.y+=.1
try:contract()
except AssertionError:negative.append('shifted pivot rejected')
else:raise AssertionError('negative pivot control accepted')
lid.location.y-=.1;bpy.context.view_layer.update();contract()
r={'status':'PASS','channel_count':len(channels),'channel_graph_connected':True,'upward_water_normals':True,'coil_count':96,'lid_dimensions':[3.72,2.38],'max_ornament_height_above_lid':.38,'negative_controls':negative,'note':'negative mutations in memory only; source never saved'}
(R/'contract-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
