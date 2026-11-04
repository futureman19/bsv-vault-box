import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'belgium.blend'),use_scripts=False);bpy.context.view_layer.update()
def check():
 lid=bpy.data.objects['Lid_Hinge'];objs=[o for o in bpy.data.objects if o.name.startswith('Fossil /')]
 assert len(objs)==69,len(objs)
 assert all(o.parent==lid for o in objs),'ornament ancestry'
 dep=bpy.context.evaluated_depsgraph_get();points=[]
 for o in objs:
  ev=o.evaluated_get(dep);m=ev.to_mesh();vs=[o.matrix_world@v.co for v in m.vertices];points.extend(vs)
  assert abs(min(v.z for v in vs)-1.978)<.00001,(o.name,'not seated',min(v.z for v in vs))
  ev.to_mesh_clear()
 assert max(abs(v.x) for v in points)<1.35 and max(abs(v.y) for v in points)<.82
 assert max(v.z for v in points)<2.35
 # Negative spaces ray through eight mid-arm angular gaps to the dark lid.
 hits=[]
 for a in range(8):
  theta=(a+.5)*math.tau/8+.1
  hit,loc,normal,idx,obj,mat=bpy.context.scene.ray_cast(dep,Vector((.58*math.cos(theta),.58*.67*math.sin(theta),3)),Vector((0,0,-1)))
  assert hit and obj.name=='Lid / polished slab',(a,obj.name)
  hits.append(obj.name)
 for n,matrix in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-matrix[i][j]) for i in range(4) for j in range(4))<1e-7
 panels=[o for o in bpy.data.objects if o.name in ['Stone / front','Stone / rear','Stone / side','Stone / side.001']];assert len(panels)==4
 # Axis aligned source panels must have no positive-volume intersections.
 for i,a in enumerate(panels):
  av=[a.matrix_world@Vector(v) for v in a.bound_box]
  for b in panels[i+1:]:
   bv=[b.matrix_world@Vector(v) for v in b.bound_box]
   overlaps=[min(max(v[k] for v in av),max(v[k] for v in bv))-max(min(v[k] for v in av),min(v[k] for v in bv)) for k in range(3)]
   assert min(overlaps)<1e-5,('panels overlap',a.name,b.name)
 return {'status':'PASS','ornament_parts':len(objs),'seated_z':1.978,'height_max':max(v.z for v in points),'gap_rays':len(hits),'pivots_unchanged':True,'panel_overlap':False}
r=check()
# Actual deliberate negative control, then restore without saving.
o=bpy.data.objects['Fossil / arm 00 segment 00'];parent=o.parent;o.parent=None
try:check()
except AssertionError as e:r['negative_control']={'detached_ornament_rejected':True,'error':str(e)}
else:raise AssertionError('negative control did not fail')
o.parent=parent
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r))
