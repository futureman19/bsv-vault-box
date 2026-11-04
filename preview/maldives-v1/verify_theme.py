import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'maldives.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def ancestry(o):
 while o.parent:
  o=o.parent
  if o==lid:return True
 return False
orn=[o for o in bpy.data.objects if o.name.startswith(('Faro /','Lagoon /','Cay /'))]
assert len(orn)==5 and all(ancestry(o) for o in orn)
reef=bpy.data.objects['Faro / raised sand reef'];lagoon=bpy.data.objects['Lagoon / inset'];cays=[o for o in orn if o.name.startswith('Cay /')]
assert len(cays)==3
# Original four-vertex section top quads have indices 1 modulo 4.
tops=[p for i,p in enumerate(reef.data.polygons[:320]) if i%4==1];assert len(tops)==80 and min(p.normal.z for p in tops)>.9
verts=[o.matrix_world@v.co for o in orn for v in o.data.vertices];assert min(v.z for v in verts)>=1.978 and max(v.z for v in verts)<=2.23
# Actual scene rays distinguish raised ring, lagoon, open channel, and outside ocean.
probes=[]
for x,y,expected in [(0,0,'Lagoon / inset'),(0,.68,'Faro / raised sand reef'),(1.2,0,'Lid / polished slab'),(1.58,0,'Lid / polished slab')]:
 hit,loc,n,idx,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and o.name==expected,(x,y,o.name if hit else None);probes.append(dict(x=x,y=y,object=o.name,z=loc.z))
# Negative control: detach real ornament, predicate must reject it, then restore.
cay=cays[0];parent=cay.parent;cay.parent=None;assert not ancestry(cay);cay.parent=parent
current={o.name:list(o.matrix_world) for o in [lid,latch]}
# Independently reopen inherited source for exact closed pivot matrix comparison.
matrices={k:[[float(x) for x in row] for row in v] for k,v in current.items()}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,m in matrices.items():assert all(abs(m[i][j]-bpy.data.objects[name].matrix_world[i][j])<1e-7 for i in range(4) for j in range(4))
result=dict(status='PASS',lid_owned_ornaments=5,cays=3,upward_reef_top_faces=80,probes=probes,detached_ornament_negative_control='PASS: rejected',base_pivots_equal=True,ornament_z_range=[min(v.z for v in verts),max(v.z for v in verts)])
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
