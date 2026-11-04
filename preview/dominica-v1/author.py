"""Dominica volcanic rainforest pilot. Authored mesh and maps; no photogrammetry.
Run maps.py first. Reproduction uses only the included trimmed mechanism.blend.
"""
import bpy,bmesh,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(521)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def maptex(m,file,input,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[input])
stonebody=mat('Volcanic stone / dark pores',(.07,.09,.08),.8);maptex(stonebody,'stone-color.png','Base Color');maptex(stonebody,'stone-roughness.png','Roughness',True)
forest=mat('Rainforest / mixed canopy',(.055,.19,.07),.9);maptex(forest,'forest-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / forest green',(.035,.07,.032),.9)
water=mat('Boiling Lake / pale grey blue',(.36,.53,.55),.24)
rimstone=mat('Basin / weathered volcanic rim',(.21,.23,.19),.88)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   normal=p.normal
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u*.4+.5,v*.4+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stonebody if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Continuous stone skins, not timber courses.
for sy in [-1,1]:cube('Volcanic body / long',(0,sy*1.145,.83),(3.72,.19,1.46),stonebody,bevel=.025)
for sx in [-1,1]:cube('Volcanic body / side',(sx*1.745,0,.83),(.23,2.10,1.46),stonebody,bevel=.025)
cube('Volcanic body / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stonebody,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stonebody,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stonebody,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def stone(n,loc,scale,p=None,material=stonebody,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Volcanic foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# A low irregular terrain with three raised rainforest knolls.
def mesh(n,verts,faces,material):
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
# Annular rocky lake rim with a real aperture, not a sphere covering water.
N=64;verts=[]
for ring in range(4):
 for i in range(N):
  a=i*math.tau/N;noise=1+.04*math.sin(7*a)+.025*math.sin(11*a)
  rx,ry,z=[(.57,.37,2.06),(.59,.39,2.18),(.73,.51,2.12),(.76,.54,1.985)][ring]
  verts.append((-.15+rx*math.cos(a)*noise,-.28+ry*math.sin(a)*noise,z+(.025*math.sin(5*a) if ring in [1,2] else 0)))
faces=[]
for r in range(3):
 for i in range(N):j=(i+1)%N;faces.append((r*N+i,r*N+j,(r+1)*N+j,(r+1)*N+i))
mesh('Lake / rocky rim',verts,faces,rimstone)
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=1,depth=.025,location=(-.15,-.28,2.0675));o=bpy.context.object;o.name='Lake / geothermal water';o.scale=(.57,.37,1);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(water);parent(o)
# Irregular heightfield islands surround rather than cover basin.
for k,(cx,cy,rx,ry,h) in enumerate([(-.95,.40,.50,.40,.47),(.0,.59,.46,.30,.59),(.88,.37,.50,.43,.44),(-1.06,-.35,.28,.40,.18),(.91,-.38,.34,.35,.17)]):
 vs=[(cx,cy,1.985+h)];rings=9;segs=40
 for j in range(1,rings+1):
  rr=j/rings
  for i in range(segs):
   a=i*math.tau/segs;irr=1+.07*math.sin(5*a+k)+.03*math.cos(9*a)
   zz=1.985+h*(1-rr**1.3)*(1+.10*math.sin(6*a+rr*8))
   vs.append((cx+rx*rr*math.cos(a)*irr,cy+ry*rr*math.sin(a)*irr,zz))
 fs=[(0,1+i,1+(i+1)%segs) for i in range(segs)]
 for j in range(rings-1):
  for i in range(segs):a=1+j*segs+i;b=1+j*segs+(i+1)%segs;fs.append((a,a+segs,b+segs,b))
 o=mesh('Rainforest / ridge '+str(k),vs,fs,forest)
 for f in o.data.polygons:f.use_smooth=True
# Compact clustered broadleaf canopy follows evaluated ridge surface.
bpy.context.view_layer.update()
from mathutils.bvhtree import BVHTree
for ridge in [o for o in bpy.data.objects if o.name.startswith('Rainforest / ridge')]:
 dep=bpy.context.evaluated_depsgraph_get();ev=ridge.evaluated_get(dep);me=ev.to_mesh();bv=BVHTree.FromPolygons([ridge.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);ev.to_mesh_clear()
 xs=[(ridge.matrix_world@v.co).x for v in ridge.data.vertices];ys=[(ridge.matrix_world@v.co).y for v in ridge.data.vertices]
 for j in range(42):
  x=random.uniform(min(xs),max(xs));y=random.uniform(min(ys),max(ys));hit=bv.ray_cast(Vector((x,y,3)),Vector((0,0,-1)))[0]
  if hit is not None and hit.z>2.04:
   stone('Rainforest / canopy',(x,y,hit.z+.02),(.075,.065,.045),lid,forest,1)
# Medallion is solid, never an unexplained front opening.
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Rounded brass','BEVEL');m.width=.005;m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name);return o
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'dominica.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'dominica.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.use_nodes=False;scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('DOMINICA AUTHORED')
