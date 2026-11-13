import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:[list(row) for row in bpy.data.objects[n].matrix_local] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'indian-ocean.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];lagoon=bpy.data.objects['Lagoon / enclosed water'];arcs=[o for o in bpy.data.objects if o.name.startswith('Reef island /')]
def check():
 assert len(arcs)==4,'four reef arcs required'
 assert all(o.parent==lid for o in [*arcs,lagoon]),'ornament detached'
 for n,m in baseline.items():assert max(abs(bpy.data.objects[n].matrix_local[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7,'pivot mismatch'
 for o in arcs:
  verts=[o.matrix_world@v.co for v in o.data.vertices]
  assert len(verts)>=80 and max(v.z for v in verts)>2.1
  assert max(abs(v.x) for v in verts)<1.4 and max(abs(v.y) for v in verts)<.8
  assert min(v.z for v in verts)>=1.97
 def ray(x,y):
  hit,loc,n,i,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
  assert hit
  return obj.name,float(loc.z)
 center=ray(0,0);assert center[0]==lagoon.name and center[1]<2.05
 passes=[ray(x,y) for x,y in [(1.1,0),(-1.1,0),(0,.6),(0,-.6)]]
 assert all(name==lagoon.name for name,z in passes),'water passes blocked'
 crown=[]
 for i in range(4):
  a=(i+.5)*math.pi/2;name,z=ray(1.1*math.cos(a),.60*math.sin(a));assert name.startswith('Reef island') and z>2.05;crown.append(z)
 return dict(center=center,passes=passes,crown_heights=crown)
result=check();original=arcs[0].parent;arcs[0].parent=None
try:check();raise RuntimeError('detachment negative control failed')
except AssertionError as e:negative=str(e)
arcs[0].parent=original;bpy.context.view_layer.update();check()
r={'status':'PASS','reef_islands':len(arcs),'rays':result,'baseline_pivots_equal':True,'all_ornaments_on_lid':True,'negative_control_detached_reef_rejected':negative,'limits':'sampled crown/center/pass rays, not ecological/geographic accuracy'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('PASS THEME',json.dumps(r))
