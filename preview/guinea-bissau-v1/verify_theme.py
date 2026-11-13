import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'guinea-bissau.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];obs=list(bpy.data.objects)
def validate():
 islands=[o for o in obs if o.name.startswith('Delta / island')];trunks=[o for o in obs if o.name.startswith('Mangrove / trunk')];roots=[o for o in obs if o.name.startswith('Mangrove / prop root')]
 assert len(islands)==4 and len(trunks)==3 and len(roots)==15
 ornament=[o for o in obs if o.name.startswith(('Delta /','Mangrove /'))]
 assert all(o.parent==lid for o in ornament),'ornament detached from lid'
 bpy.context.view_layer.update()
 verts=[o.matrix_world@v.co for o in ornament for v in o.data.vertices]
 assert max(v.z for v in verts)<2.978
 # Tubes store world-space coordinates in their mesh, not object location.
 assert all(min((o.matrix_world@v.co).x for v in o.data.vertices)>0 and min((o.matrix_world@v.co).y for v in o.data.vertices)>0 for o in trunks)
 # Each root's lowest vertex must enter the island volume; vertical ray finds sand above it.
 from mathutils.bvhtree import BVHTree
 vs=[];fs=[]
 for o in islands:
  offset=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices);fs.extend(tuple(offset+i for i in p.vertices) for p in o.data.polygons)
 tree=BVHTree.FromPolygons(vs,fs);contacts=[]
 for o in roots:
  low=min((o.matrix_world@v.co for v in o.data.vertices),key=lambda v:v.z)
  loc,normal,index,d=tree.ray_cast(Vector((low.x,low.y,3)),Vector((0,0,-1)))
  assert loc is not None and loc.z>=low.z and loc.z-low.z<.2,(o.name,loc,low)
  contacts.append(loc.z-low.z)
 assert bpy.data.materials['Lagoon / tidal teal'].diffuse_color[1]>bpy.data.materials['Lagoon / tidal teal'].diffuse_color[0]*3
 return dict(islands=len(islands),trunks=len(trunks),prop_roots=len(roots),ornaments=len(ornament),all_parented=True,root_sand_penetration=contacts,maximum_ornament_z=max(v.z for v in verts))
result=validate()
o=next(o for o in obs if o.name.startswith('Delta / island'));o.parent=None
try:validate()
except AssertionError as e:result['negative_detached_island']='REJECTED: '+str(e)
else:raise AssertionError('Negative control incorrectly passed')
result['status']='PASS';(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
