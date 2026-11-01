"""Independent saved-source comparison and measured feature gates, not author tags."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
mutable=('Basalt fracture','Sheltered moss v7','River /','Glacier /','Lid / polished slab')
def snapshot():
 bpy.context.view_layer.update();out={};trees={}
 for o in bpy.data.objects:
  if o.type!='MESH':continue
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();vs=[o.matrix_world@v.co for v in me.vertices];fs=[list(p.vertices) for p in me.polygons]
  out[o.name]={'v':[tuple(v) for v in vs],'f':fs,'parent':o.parent.name if o.parent else None};trees[o.name]=BVHTree.FromPolygons(vs,fs);ev.to_mesh_clear()
 return out,trees
bpy.ops.wm.open_mainfile(filepath=str(R/'approved-v7.blend'),use_scripts=False);old,ot=snapshot()
bpy.ops.wm.open_mainfile(filepath=str(R/'iceland.blend'),use_scripts=False);new,nt=snapshot()
preserved=[n for n in old if not n.startswith(mutable)];assert all(new[n]==old[n] for n in preserved)
# Direct two-sided ray comparison over old cladding footprints measures actual removed volume.
removed={s:[] for s in ['front','rear','left','right']};changed=[]
for name,record in old.items():
 if not name.startswith('Basalt fracture'):continue
 side=name.split('/ ')[1].split('.')[0];axis=1 if side in ['front','rear'] else 0;tan=1-axis;sgn=-1 if side in ['front','left'] else 1
 vv=record['v'];lo=[min(v[a] for v in vv) for a in range(3)];hi=[max(v[a] for v in vv) for a in range(3)];depths=[]
 for i in range(21):
  for j in range(25):
   origin=Vector((0,0,0));origin[axis]=sgn*3;origin[tan]=lo[tan]+(hi[tan]-lo[tan])*(i+.5)/21;origin.z=lo[2]+(hi[2]-lo[2])*(j+.5)/25;direction=Vector((0,0,0));direction[axis]=-sgn
   a,_,_,_=ot[name].ray_cast(origin,direction,4);b,_,_,_=nt[name].ray_cast(origin,direction,4)
   if a is not None and b is not None and (a[axis]-b[axis])*sgn>.003:depths.append((a[axis]-b[axis])*sgn)
 if depths:removed[side].extend(depths);changed.append(name)
assert all(len(v)>20 and max(v)>.045 for v in removed.values()),{k:(len(v),max(v or [0])) for k,v in removed.items()}
# Identical liner solids plus wall intersections at multiple interior heights.
shell=[]
for z in [.35,.7,1.05,1.4]:
 for axis in [0,1]:
  for sign in [-1,1]:
   for along in [-.65,0,.65]:
    origin=Vector((0,0,z));origin[1-axis]=along;d=Vector((0,0,0));d[axis]=sign
    hits=[t.ray_cast(origin,d,2.1)[0] for n,t in nt.items() if n.startswith('Interior wall')];assert any(x is not None for x in hits);shell.append([z,axis,sign,along])
water=next(o for o in bpy.data.objects if o.name.startswith('River / depth'));cascade=next(o for o in bpy.data.objects if o.name.startswith('River / connected'));glacier=next(o for o in bpy.data.objects if o.name.startswith('Glacier /'))
w=[water.matrix_world@v.co for v in water.data.vertices];c=[cascade.matrix_world@v.co for v in cascade.data.vertices];g=[glacier.matrix_world@v.co for v in glacier.data.vertices]
join=max((w[i]-c[i]).length for i in range(6));assert join<1e-6
widths=[(w[i+5]-w[i]).length for i in range(0,len(w),6)];assert max(widths)/min(widths)>1.3
zs=[v.z for v in g];assert max(zs)-min(zs)>.25
# Glacier footprint overlaps upstream river, outlet channel lies directly beneath ice.
up=w[-3];hit=nt[glacier.name].ray_cast(Vector((up.x,up.y,3)),Vector((0,0,-1)),2)[0];assert hit is not None
r={'unchanged_evaluated_mesh_records':len(preserved),'unchanged_shell_and_hardware':True,'changed_basalt_blocks_with_measured_recess':len(changed),'recess_rays':{s:{'count':len(v),'minimum':min(v),'maximum':max(v),'mean':sum(v)/len(v)} for s,v in removed.items()},'wall_rays':len(shell),'river_cascade_join_max':join,'river_width_min_max':[min(widths),max(widths)],'ice_relief':max(zs)-min(zs),'ice_overlaps_upstream':True,'all_ice_water_lid_parented':all(o.parent.name=='Lid_Hinge' for o in [water,cascade,glacier])}
(R/'geometry-features-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
