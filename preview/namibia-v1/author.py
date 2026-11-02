"""Namib Dune Sea: script-authored Blender collectible; prior mechanism read-only."""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(1430)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.preferences.filepaths.save_version=0
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def linear(c):return ((c+.055)/1.055)**2.4 if c>.04045 else c/12.92
def mat(n,h,r=.7,metal=0):
 c=tuple(linear(int(h[i:i+2],16)/255) for i in (0,2,4));m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,file,input):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if input!='Base Color':t.image.colorspace_settings.name='Non-Color'
 t.image.pack();p=m.node_tree.nodes.get('Principled BSDF')
 if input=='Normal':
  norm=m.node_tree.nodes.new('ShaderNodeNormalMap');norm.inputs['Strength'].default_value=.35;m.node_tree.links.new(t.outputs['Color'],norm.inputs['Color']);m.node_tree.links.new(norm.outputs['Normal'],p.inputs[input])
 else:m.node_tree.links.new(t.outputs['Color'],p.inputs[input])
sand=mat('Sand / wind ripples','AA542D');tex(sand,'sand-color.png','Base Color');tex(sand,'sand-roughness.png','Roughness');tex(sand,'sand-normal.png','Normal')
dune=mat('Dune / sunlit ochre','CE773B',.85);tex(dune,'sand-roughness.png','Roughness');tex(dune,'sand-normal.png','Normal')
rim=mat('Lid / satin iron-rich mineral','763B28',.4)
pan=mat('Playa / pale mineral pan','DDD0AA',.91)
inner=mat('Interior / dark mineral liner','3B2821',.65)
gold=mat('Brass / aged satin','B38C4D',.32,.78)
seam=mat('Seam / dark umber','35271F',.9)
foot=mat('Feet / dark mineral','44342C',.85)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Planar mineral UV')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(p.normal.z)>.7:u,v=co.x/3.72,co.y/2.38
   elif abs(p.normal.x)>.7:u,v=co.y/2.38,co.z/1.46
   else:u,v=co.x/3.72,co.z/1.46
   layer.data[li].uv=(u+.5,v+.5)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Soft edges','BEVEL');mod.width=min(bevel,min(dim)*.35);mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(inner if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Continuous exterior shells rather than cedar courses or geological strata.
for sy in [-1,1]:cube('Sand body / front' if sy<0 else 'Sand body / rear',(0,sy*1.145,.83),(3.72,.19,1.46),sand,bevel=.035)
for sx in [-1,1]:cube('Sand body / side',(sx*1.745,0,.83),(.23,2.10,1.46),sand,bevel=.028)
cube('Sand body / clasp seat',(0,-1.255,1.36),(.56,.075,.47),sand,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.09),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.09),seam,bevel=.009)
 for sy in [-1,1]:cube('Sand body / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),sand,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),rim,lid,.045)
# A thin warm sand bed is the lid surface, not a raised rectangular terrain block.
cube('Lid / sand field',(0,0,1.982),(3.43,2.09,.016),sand,lid,.005)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(sx*1.47,sy*.91,-.10));o=bpy.context.object;o.name='Mineral foot'
  for v in o.data.vertices:v.co=Vector((v.co.x*.32,v.co.y*.27,v.co.z*.19))*(1+random.uniform(-.08,.08))
  o.data.materials.append(foot)
# Three asymmetric curved crests, tapering naturally into the sand bed.
for k,(cy,height,phase) in enumerate([(-.65,.25,0),(0,.40,.9),(.62,.54,1.7)]):
 verts=[];faces=[];nx=72;ny=20
 for i in range(nx+1):
  t=i/nx;x=-1.55+(1.70 if k==0 else 3.10)*t;envelope=math.sin(math.pi*t)**.75
  center=cy+.095*math.sin(t*6+phase);width=.24+.04*math.sin(t*4+phase)
  for j in range(ny+1):
   v=j/ny;cross=(v-.58)/(.58 if v<=.58 else .42)
   profile=max(0,1-abs(cross))**(.8 if v<=.58 else 1.15)
   z=1.99+height*envelope*profile
   verts.append((x,center+(v-.5)*2*width,z))
 for i in range(nx):
  for j in range(ny):a=i*(ny+1)+j;faces.append((a,a+ny+1,a+ny+2,a+1))
 me=bpy.data.meshes.new('Curved asymmetric dune');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Dune ridge / '+str(k+1),me);bpy.context.collection.objects.link(o);me.materials.append(dune);uv(o);parent(o)
 for p in me.polygons:p.use_smooth=True
 o['crest_height']=height
# Irregular ivory playa between the front two dunes, original generated outline.
verts=[(.93,-.65,1.995)];N=80
for j in range(N):
 a=j*math.tau/N;r=1+.08*math.sin(a*5)+.04*math.sin(a*9)
 verts.append((.93+math.cos(a)*.60*r,-.65+math.sin(a)*.25*r,1.995))
faces=[(0,j+1,(j+1)%N+1) for j in range(N)];me=bpy.data.meshes.new('Irregular playa');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Playa / ivory basin',me);bpy.context.collection.objects.link(o);me.materials.append(pan);parent(o)
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Rounded brass','BEVEL');m.width=min(.005,depth*.35);m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name)
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.4));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.12))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'namibia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'namibia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('NAMIBIA AUTHORED')
