import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'senegal.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
orn=[o for o in bpy.data.objects if o.name.startswith(('Mangrove /','Saloum /'))]
def ancestry():
 assert all(o.parent==lid for o in orn),'detached ornament'
ancestry();bad=orn[0];mw=bad.matrix_world.copy();bad.parent=None
try:ancestry()
except AssertionError:negative=True
else:negative=False
bad.parent=lid;bad.matrix_world=mw;bpy.context.view_layer.update();assert negative;ancestry()
banks=[o for o in orn if o.name.startswith('Saloum / bank')];roots=[o for o in orn if o.name.startswith('Mangrove / root')];trunks=[o for o in orn if o.name.startswith('Mangrove / trunk')]
assert len(banks)==3 and len(roots)==24 and len(trunks)==6
assert max((o.matrix_world@v.co).z for o in orn for v in o.data.vertices)<2.65
# Exposed root outer end centre is the mean first ring of the authored tube.
seating=[]
for o in roots:
 c=sum((o.matrix_world@v.co for v in list(o.data.vertices)[:9]),Vector())/9
 hits=[]
 for b in banks:
  inv=b.matrix_world.inverted();hit,loc,n,idx=b.ray_cast(inv@Vector((c.x,c.y,3)),Vector((0,0,-1)))
  if hit:hits.append((b.matrix_world@loc).z)
 assert hits and abs(c.z-max(hits))<=.012,(o.name,tuple(c),hits)
 seating.append(abs(c.z-max(hits)))
# Specific Y-channel exposed-water centreline rays, independently enumerated.
pts=[(-.10,-.65),(-.10,-.45),(-.10,-.25),(-.1,0),(-.1,.18),(-.17,.35),(-.2,.55),(.1,0),(.35,-.09),(.6,-.06),(.85,.01),(1.1,.035),(1.4,.02)]
water=[]
for x,y in pts:
 hit,loc,n,idx,o,mat=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 water.append({'xy':[x,y],'object':o.name if o else None});assert hit and o.name=='Saloum / water',water[-1]
# Source pivot equality to included untouched trimmed family mechanism.
actual={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(actual[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in actual for i in range(4) for j in range(4));assert err<1e-7
out={'status':'PASS','banks':len(banks),'trees':len(trunks),'roots':len(roots),'lid_owned_ornaments':len(orn),'detached_ornament_negative_control_rejected':negative,'root_max_seating_gap':max(seating),'water_channel_rays':water,'pivot_max_error':err,'limitations':'Enumerated visible channel samples, not geographic/hydrologic accuracy or continuous clearance.'}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
