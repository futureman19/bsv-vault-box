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
stone_mat=mat('Svaneti / weathered stone',(.26,.22,.16),.8)
maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
t=stone_mat.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/stone-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();normal=stone_mat.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.3;stone_mat.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);stone_mat.node_tree.links.new(normal.outputs['Normal'],stone_mat.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / alpine green',(.035,.06,.029),.9)
snow=mat('Ridge / chalk snow',(.82,.87,.86),.85)
rock=mat('Ridge / charcoal schist',(.17,.19,.17),.95)
olive=mat('Ridge / alpine olive',(.12,.16,.055),.95)
dark=mat('Tower / recessed shadow',(.025,.029,.026),1)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Staggered actual masonry courses, with narrow seams over continuous liner.
for row in range(6):
 z=.10+(row+.5)*1.46/6;h=1.46/6-.012
 for sy in [-1,1]:
  edges=[-1.86]+[q for q in [-1.24+(.25 if row%2 else 0),-.62+(.25 if row%2 else 0),0+(.25 if row%2 else 0),.62+(.25 if row%2 else 0),1.24+(.25 if row%2 else 0)] if -1.86<q<1.86]+[1.86]
  for i in range(len(edges)-1):cube('Masonry / course',((edges[i]+edges[i+1])/2,sy*1.145,z),(edges[i+1]-edges[i]-.012,.19,h),stone_mat,bevel=.009)
 for sx in [-1,1]:
  for i in range(4):cube('Masonry / side',(sx*1.745,-.7875+i*.525,z),(.23,.513,h),stone_mat,bevel=.009,axis='Y')
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.09),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.09),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone foot',(sx*1.47,sy*.91,-.08),(.5,.42,.30),rock,bevel=.06)
# Irregular triangular ridge surface, continuous with lid at its perimeter.
verts=[];faces=[];nx=31;ny=17
for j in range(ny):
 for i in range(nx):
  x=-1.35+i*2.7/(nx-1);y=-.12+j*1.10/(ny-1)
  edge=math.sin(math.pi*i/(nx-1))*math.sin(math.pi*j/(ny-1))
  peaks=.42+.24*math.sin(x*4.7)+.16*math.sin(x*8.2+.7)
  z=1.978+max(0,edge)*(peaks+random.uniform(-.07,.07))
  verts.append((x,y,z))
for j in range(ny-1):
 for i in range(nx-1):
  q=j*nx+i;faces.extend([(q,q+1,q+nx+1),(q,q+nx+1,q+nx)])
me=bpy.data.meshes.new('Alpine triangular relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Svaneti snow ridge',me);bpy.context.collection.objects.link(o)
for m in [rock,snow,olive]:me.materials.append(m)
for f in me.polygons:
 z=sum(me.vertices[v].co.z for v in f.vertices)/3
 f.material_index=1 if z>2.30+random.uniform(-.04,.04) else (2 if z<2.12 and random.random()<.55 else 0)
parent(o)
# Tapering tower, three dark slit levels and a gabled stone cap.
def mesh(n,vs,fs,material):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
cx=-.85;cy=-.57;z0=1.978;zt=2.67
vs=[(cx+sx*w,cy+sy*w,z) for z,w in [(z0,.17),(zt,.125)] for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
mesh('Tower / tapered stone',vs,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],stone_mat)
for i in range(3):
 z=2.12+i*.17;w=.17-(z-z0)/(.692)*.045
 cube('Tower / slit', (cx,cy-w-.002,z),(.038,.008,.075),dark,lid,.002)
mesh('Tower / gabled cap',[(cx-.155,cy-.155,zt),(cx+.155,cy-.155,zt),(cx+.155,cy+.155,zt),(cx-.155,cy+.155,zt),(cx,cy-.155,zt+.10),(cx,cy+.155,zt+.10)],[(0,1,4),(3,5,2),(0,4,5,3),(4,1,2,5),(0,3,2,1)],rock)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'georgia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'georgia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('GEORGIA AUTHORED')
