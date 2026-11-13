import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'armenia.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
arches=[o for o in bpy.data.objects if o.name.startswith('Arcade / arch')];piers=[o for o in bpy.data.objects if o.name.startswith('Arcade / pier')]
def ownership():return len(arches)==3 and len(piers)==6 and all(o.parent==lid for o in arches+piers)
assert ownership()
o=arches[0];o.parent=None;negative=not ownership();o.parent=lid;assert negative and ownership()
# Preserve exact baseline pivots using a second file open after gathering values.
pivots={o.name:[list(row) for row in o.matrix_local] for o in [lid,latch]}
dep=bpy.context.evaluated_depsgraph_get();probes=[]
for cx in [-.95,0,.95]:
 for z,want in [(2.43,False),(2.66,True)]:
  hits=[]
  for o in arches+piers:
   inv=o.matrix_world.inverted();origin=inv@Vector((cx,-1,z));direction=(inv.to_3x3()@Vector((0,1,0))).normalized();ev=o.evaluated_get(dep);hit,*_=ev.ray_cast(origin,direction)
   if hit:hits.append(o.name)
  assert bool(hits)==want,(cx,z,hits);probes.append({'x':cx,'z':z,'hits':hits})
verts=[o.matrix_world@v.co for o in arches+piers for v in o.data.vertices];zmin=min(v.z for v in verts);zmax=max(v.z for v in verts)
assert abs(zmin-1.978)<1e-5 and zmax<2.75
im=bpy.data.images.get('tuff-color.png');assert im and im.packed_file
pix=list(im.pixels);means=[sum(pix[c::4])/(len(pix)/4) for c in range(3)];assert means[0]>means[1]>means[2]
assert max(pix[0::4])-min(pix[0::4])>.1
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,matrix in pivots.items():
 assert max(abs(matrix[i][j]-bpy.data.objects[name].matrix_local[i][j]) for i in range(4) for j in range(4))<1e-7
r={'status':'PASS','arches':3,'piers':6,'aperture_and_crown_rays':probes,'lid_ownership_negative_control_rejected':negative,'ornament_z_bounds':[zmin,zmax],'exact_inherited_pivots':True,'rose_map_mean_rgb':means}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
