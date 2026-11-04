"""Uruguay brief-led procedural landscape collectible; no photogrammetry.
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
stonebody=mat('Uruguay / earthy mineral',(.25,.28,.24),.83);maptex(stonebody,'mineral-color.png','Base Color');maptex(stonebody,'mineral-roughness.png','Roughness',True)
wood=stonebody
granite=mat('Uruguay / gray foot',(.22,.24,.21),.88);maptex(granite,'mineral-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / dark green',(.025,.055,.025),.9)
grass=mat('Grassland / olive green',(.23,.30,.075),.92);maptex(grass,'grass-color.png','Base Color')
rock=mat('Gorge / exposed mineral',(.24,.22,.15),.9)
water=mat('Yerbal / blue green',(.028,.24,.26),.20,.1)
forest=mat('Gallery forest / deep green',(.045,.105,.025),.95)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Mineral planar')
 for p in o.data.polygons:
  normal=p.normal;major=max(range(3),key=lambda k:abs(normal[k]));axes=[k for k in range(3) if k!=major]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.5+.5,co[axes[1]]*.5+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Broad stone skins; continuous liner is inherited behind them.
for sy in [-1,1]:cube('Mineral body / long',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Mineral body / end',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025,axis='Y')
# Small collar fills the central clasp mounting behind its retained position.
cube('Mineral / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Mineral / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
# Restrained brass corner protectors replace the Iceland wraps entirely.
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def stone(n,loc,scale,p=None,material=granite,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Mineral foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Two continuous irregular banks, sloping from raised prairie into a lower gorge.
def center(y):return .26*math.sin(3*y)
def height(t,y):return 2.00+(.16+.18*math.sin((y+.95)*1.8)**2)*math.sin(math.pi*t)**.65
for side in [-1,1]:
 vs=[];fs=[];ny=36;nx=12
 for j in range(ny+1):
  y=-.88+1.76*j/ny
  for i in range(nx+1):
   t=i/nx;inner=center(y)+side*.17;x=inner+(side*1.50-inner)*t
   z=1.974 if i==nx else (2.00 if i==0 else height(t,y))
   vs.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;face=(a,a+1,a+nx+2,a+nx+1)
   fs.append(face if side>0 else tuple(reversed(face)))
 me=bpy.data.meshes.new('Grassland grid');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Terrain / grassland bank '+str(side),me);bpy.context.collection.objects.link(o);me.materials.append(grass);me.materials.append(rock)
 for f in me.polygons:f.material_index=1 if f.index%nx<2 else 0;f.use_smooth=True
 uv(o);parent(o)
# The continuous ribbon lies below bank crowns, with no holes or disconnected pools.
vs=[];fs=[]
for j in range(49):
 y=-.88+1.76*j/48;x=center(y);vs.extend([(x-.145,y,2.025),(x+.145,y,2.025)])
for j in range(48):a=j*2;fs.append((a,a+1,a+3,a+2))
me=bpy.data.meshes.new('Winding water ribbon');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Terrain / Yerbal stream',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
for side in [-1,1]:
 for j in range(9):
  y=-.72+j*.18;t=.18+.035*math.sin(j*2);inner=center(y)+side*.17;x=inner+(side*1.50-inner)*t
  stone('Terrain / gallery scrub',(x,y,height(t,y)+.018),(.095,.08,.065),lid,forest,2)
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.3));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'uruguay.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'uruguay.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('URUGUAY AUTHORED')
