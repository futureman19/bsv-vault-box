"""Brief-led Vanuatu pilot. Authored mesh and maps; no photogrammetry.
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
ash=mat('Ash stone / porous charcoal',(.065,.058,.05),.82)
maptex(ash,'ash-color.png','Base Color');maptex(ash,'ash-roughness.png','Roughness',True)
t=ash.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/ash-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack()
n=ash.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.28;ash.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);ash.node_tree.links.new(n.outputs['Normal'],ash.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
wood=ash;granite=ash
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Oxidized mineral seam',(.10,.035,.018),.9)
ember=mat('Ember / restrained orange',(.55,.11,.012),.72)
p=ember.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(.7,.055,.003,1);p.inputs['Emission Strength'].default_value=.28
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   # Dominant-face projection keeps mineral grain isotropic on side faces.
   normal=p.normal
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/1.7+.5,v/1.7+.5)
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
for sy in [-1,1]:cube('Ash / front' if sy<0 else 'Ash / rear',(0,sy*1.145,.83),(3.72,.19,1.46),ash,bevel=.018)
for sx in [-1,1]:cube('Ash / side',(sx*1.745,0,.83),(.23,2.10,1.46),ash,bevel=.018)
# Small collar fills the central clasp mounting behind its retained position.
cube('Ash / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Oxide seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Oxide seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Ash / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
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
 for sy in [-1,1]:stone('Volcanic foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Broad crater: radial outer apron, irregular crown and descending inner bowl.
verts=[];faces=[];N=96
# radius X, radius Y, nominal height; every ring remains distinctly separated.
rings=[(1.30,.83,1.985),(1.08,.70,2.12),(.76,.52,2.40),(.57,.41,2.61),(.40,.29,2.46),(.30,.22,2.135)]
for k,(rx,ry,z) in enumerate(rings):
 for j in range(N):
  angle=j*math.tau/N;wave=.045*math.sin(angle*3+.2)+.022*math.sin(angle*7)
  irregular=1+.035*math.sin(angle*5)+.018*math.cos(angle*11)
  verts.append((rx*math.cos(angle)*irregular, .12+ry*math.sin(angle)*irregular,z+(wave if k in [2,3,4] else .008*math.sin(angle*6))))
for k in range(len(rings)-1):
 for j in range(N):
  a=k*N+j;b=k*N+(j+1)%N;c=(k+1)*N+(j+1)%N;d=(k+1)*N+j
  faces.extend([(a,b,d),(b,c,d)])
me=bpy.data.meshes.new('Yasur crater radial relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Yasur recessed crater',me);bpy.context.collection.objects.link(o);me.materials.append(ash);uv(o);parent(o)
# Dark glowing basin closes the bowl without a false solid summit.
verts=[(0,.12,2.13)]+[(.302*math.cos(j*math.tau/N),.12+.222*math.sin(j*math.tau/N),2.13) for j in range(N)]
faces=[(0,1+j,1+(j+1)%N) for j in range(N)]
me=bpy.data.meshes.new('Ember basin');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Ember basin',me);bpy.context.collection.objects.link(o);me.materials.append(ember);parent(o)
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.4));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'vanuatu.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'vanuatu.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('VANUATU AUTHORED')
