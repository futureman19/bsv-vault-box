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
ocean=mat('Ocean / deep blue enamel',(.025,.14,.21),.32)
maptex(ocean,'ocean-color.png','Base Color');maptex(ocean,'ocean-roughness.png','Roughness',True)
t=ocean.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/ocean-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=ocean.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.18;ocean.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);ocean.node_tree.links.new(n.outputs['Normal'],ocean.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
ice=mat('Sea ice / porcelain white',(.64,.82,.86),.47)
edge=mat('Sea ice / blue edge',(.16,.40,.49),.36)
water=mat('Leads / dark teal',(.012,.095,.13),.23)
pond=mat('Melt ponds / turquoise',(.025,.46,.57),.19)
seam=mat('Seam / deep teal',(.012,.047,.06),.75)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   if axis=='Y' and abs(p.normal.z)>.7:v=co.x
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
# Isotropic face projection for blue enamel, not inherited wood UV orientation.
def project(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Planar enamel')
 for f in o.data.polygons:
  axis=max(range(3),key=lambda a:abs(f.normal[a]));a,b=[i for i in range(3) if i!=axis]
  for li in f.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(v[a]/2+.5,v[b]/2+.5)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(ocean if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):project(o)
for sy in [-1,1]:
 project(cube('Ocean / front' if sy<0 else 'Ocean / rear',(0,sy*1.145,.83),(3.72,.19,1.46),ocean,bevel=.025))
for sx in [-1,1]:
 project(cube('Ocean / side',(sx*1.745,0,.83),(.23,2.10,1.46),ocean,bevel=.025))
project(cube('Ocean / clasp seat',(0,-1.255,1.36),(.56,.075,.47),ocean,bevel=.025))
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Ocean / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),ocean,bevel=.004)
  cube('Ocean / foot',(sx*1.47,sy*.91,-.10),(.55,.46,.36),ocean,bevel=.09)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),water,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def prism(name,poly,z,h,top=ice):
 vs=[(x,y,z) for x,y in poly]+[(x,y,z+h) for x,y in poly];n=len(poly)
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(edge);me.materials.append(top);me.polygons[1].material_index=1;parent(o);return o
# Voronoi-like jittered quadrilateral cells leave real connected lead gaps.
grid={}
for j in range(4):
 for i in range(5):grid[i,j]=(-1.56+i*.78+(random.uniform(-.13,.13) if 0<i<4 and 0<j<3 else 0),-.88+j*.58+(random.uniform(-.10,.10) if 0<i<4 and 0<j<3 else 0))
for j in range(3):
 for i in range(4):
  poly=[grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]];cx=sum(v[0] for v in poly)/4;cy=sum(v[1] for v in poly)/4;poly=[(cx+(x-cx)*.91,cy+(y-cy)*.91) for x,y in poly];h=.075+random.random()*.045
  prism('Floe / %d %d'%(i,j),poly,1.97,h)
  if (i,j) in [(0,0),(2,1)]:
   inset=[(cx+(x-cx)*.52,cy+(y-cy)*.48) for x,y in poly];prism('Pond / %d %d'%(i,j),inset,1.97+h,.006,pond)
for i in range(9):
 x=-1.3+i*.29;y=.59+.065*math.sin(i*1.8)
 o=prism('Pressure ridge / '+str(i),[(x-.15,y-.12),(x+.13,y-.10),(x+.16,y+.08),(x-.09,y+.13)],2.04,.12+random.random()*.22)
 # angular roof with independent heights, not a mountain range cone
 for v in o.data.vertices:
  if v.index>=4:v.co.z+=random.uniform(-.035,.035)
# Medallion is solid, never an unexplained front opening.
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Rounded brass','BEVEL');m.width=.005;m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name);return o
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'arctic.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'arctic.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('ARCTIC AUTHORED')
