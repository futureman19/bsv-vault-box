"""Moss-only addition to immutable approved v6 source. No relighting or other edits."""
from pathlib import Path
import bpy,random,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'approved-v6.blend'),use_scripts=False)
rng=random.Random(707)
bpy.context.view_layer.update()
# Ray-conform patches to the original fractured surface, including sheltered ledges.
vs=[];fs=[]
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.startswith(('Basalt fracture','Interior wall')):
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();off=len(vs)
  vs.extend([o.matrix_world@v.co for v in m.vertices]);fs.extend([tuple(off+i for i in p.vertices) for p in m.polygons]);ev.to_mesh_clear()
rock=BVHTree.FromPolygons(vs,fs)
colors=[(.085,.155,.023,1),(.125,.205,.033,1),(.17,.235,.052,1),(.25,.285,.155,1)]
mats=[]
for i,col in enumerate(colors):
 m=bpy.data.materials.new('Moss v7 / '+['forest cushion','olive frond','sunlit tips','pale lichen'][i]);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.92;m.diffuse_color=col;mats.append(m)
# Hand-selected clusters: interrupted joints; central clasp and corner guards excluded.
patches=[('front',-1.21,.48,.16,.16),('front',-.83,.76,.15,.18),('front',-.54,.33,.19,.16),('front',-.37,.62,.12,.20),('front',.53,.43,.18,.18),('front',.90,.78,.16,.18),('front',1.27,.40,.12,.15),('front',-1.16,1.14,.10,.12),('front',.61,1.20,.09,.12),('left',-.69,.56,.16,.18),('left',-.36,.34,.17,.15),('left',.32,.56,.15,.20),('left',.60,.93,.12,.18),('left',-.52,1.20,.11,.11),('right',-.55,.48,.14,.19),('rear',.65,.56,.14,.17)]
new=[]
for index,(side,u,z,wu,hz) in enumerate(patches):
 vertices=[];faces=[];mi=[]
 normal=Vector((0,-1,0) if side=='front' else ((-1,0,0) if side=='left' else ((1,0,0) if side=='right' else (0,1,0))))
 tangent=Vector((1,0,0) if side in ('front','rear') else (0,1,0));up=Vector((0,0,1))
 def surface(a,b):
  origin=tangent*a+up*b+normal*3
  hit,_,_,_=rock.ray_cast(origin,-normal,4)
  return hit
 for lobe in range(48):
  # Vertical branching distribution, not a circular patch or uniform dot grid.
  t=rng.uniform(-1,1);a=u+wu*(.32*math.sin(t*5+index)+rng.uniform(-.50,.50));b=z+hz*t
  hit=surface(a,b)
  if hit is None:continue
  rad=rng.uniform(.019,.043);elong=rng.uniform(.65,1.25);height=rng.uniform(.009,.024)
  k=len(vertices);vertices.append(hit+normal*height)
  for j in range(7):
   angle=math.tau*j/7;rr=rad*rng.uniform(.65,1.15);aa=a+math.cos(angle)*rr;bb=b+math.sin(angle)*rr*elong
   # Follow stone without spanning abrupt fracture depths as stretched triangles.
   edge=surface(aa,bb)
   if edge is None or abs((edge-hit).dot(normal))>.05:edge=hit+tangent*(aa-a)+up*(bb-b)
   vertices.append(edge+normal*rng.uniform(.003,.009))
  color=rng.choices([0,1,2,3],[26,49,22,3])[0]
  for j in range(7):faces.append((k,k+1+j,k+1+(j+1)%7));mi.append(color)
  # Fine irregular short branching tips, compact rather than tall grass.
  for q in range(3):
   a0=rng.uniform(0,math.tau);base=hit+normal*height+tangent*(rad*.6*math.cos(a0))+up*(rad*.6*math.sin(a0));tip=base+up*rng.uniform(.009,.023)+normal*.004+tangent*rng.uniform(-.009,.009)
   w=rng.uniform(.0016,.003);kk=len(vertices);vertices.extend([base-tangent*w,base+tangent*w,tip,tip+up*.006+tangent*.004]);faces.extend([(kk,kk+1,kk+2),(kk+1,kk+3,kk+2)]);mi.extend([color,color])
 me=bpy.data.meshes.new('Moss v7 / branching recess mat');me.from_pydata(vertices,[],faces);me.update();ob=bpy.data.objects.new('Sheltered moss v7 / '+side+' '+str(index),me);bpy.context.collection.objects.link(ob)
 for m in mats:me.materials.append(m)
 for p,i in zip(me.polygons,mi):p.material_index=i;p.use_smooth=True
 ob['growth']='low irregular ray-conformed compact lobes and short fibers';new.append(ob.name)
# Scene, camera, lighting, old meshes, all old material nodes and articulation unchanged.
bpy.ops.wm.save_as_mainfile(filepath=str(R/'iceland.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ('MESH','EMPTY'):o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Lid_Hinge']
bpy.ops.export_scene.gltf(filepath=str(R/'iceland.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
import runpy
runpy.run_path(str(R/'merge_moss.py'))
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
(R/'moss-authorship.json').write_text(json.dumps({'new_patches':new,'seed':707,'unchanged_baseline':'approved-v6.blend','approach':'additive moss-only ray-conformed lobes and fibers'},indent=2))
print('MOSS_V7_EXPORTED',len(new))
