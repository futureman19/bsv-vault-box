"""Brief-led Luxembourg pilot. Authored geometry and maps; no photogrammetry.
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
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   n=p.normal
   u,v=(co.y,co.z) if abs(n.x)>.7 else ((co.x,co.y) if abs(n.z)>.7 else (co.x,co.z))
   layer.data[li].uv=(u/1.5+.5,v/1.5+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
stone=mat('Sandstone / buff sediment',(.5,.4,.25),.8);maptex(stone,'sandstone-color.png','Base Color');maptex(stone,'sandstone-roughness.png','Roughness',True)
t=stone.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/sandstone-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=stone.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.3;stone.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);stone.node_tree.links.new(n.outputs['Normal'],stone.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
green=mat('Fern / shaded olive',(.055,.12,.025),.92);dark=mat('Seam / dark olive',(.03,.055,.018),.9);water=mat('Ravine / blue green stream',(.035,.17,.16),.23)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Sandstone / front' if sy<0 else 'Sandstone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.035)
for sx in [-1,1]:cube('Sandstone / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.035)
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),dark,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),dark,bevel=.009)
 for sy in [-1,1]:cube('Sandstone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Sandstone / foot',(sx*1.47,sy*.91,-.07),(.50,.43,.30),stone,bevel=.08)
# Each rocky wall has an irregular polygon footprint, layered ledges and a clear ravine.
for side in [-1,1]:
 for level in range(4):
  z=1.97+level*.15;cx=side*(.64+level*.025)
  poly=[(-.39,-.74),(.28,-.68),(.43,-.28),(.35,.35),(.22,.67),(-.30,.73),(-.45,.24),(-.37,-.32)]
  verts=[]
  for top in [0,1]:
   for j,(x,y) in enumerate(poly):verts.append((cx+x*(1-level*.06),y*(1-level*.03),z+top*(.16+(.025*math.sin(j*2.4+level) if level==3 else 0))))
  faces=[tuple(reversed(range(8))),tuple(range(8,16))]+[(j,(j+1)%8,(j+1)%8+8,j+8) for j in range(8)]
  me=bpy.data.meshes.new('Eroded outcrop');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Outcrop / '+('west' if side<0 else 'east')+' '+str(level),me);bpy.context.collection.objects.link(o);me.materials.append(stone);uv(o);parent(o)
cube('Ravine / stream',(0,0,1.991),(.24,1.43,.018),water,lid,.006)
# Small pinnate fern fans, rooted on exposed lid shoulders, not tree substitutes.
for k in range(12):
 sx=-1 if k%2 else 1;x=sx*(1.13+random.random()*.13);y=-.60+(k//2)*.23
 verts=[];faces=[]
 for f in range(5):
  a=f*math.tau/5;length=.22+random.random()*.09
  stem=[]
  for j in range(7):
   t=j/6;c=Vector((x+math.cos(a)*length*t,y+math.sin(a)*length*t,1.975+.23*math.sin(t*2)));w=Vector((-math.sin(a),math.cos(a),0))*.006;i=len(verts);verts.extend([c-w,c+w]);stem.append(i)
   if j:faces.append((stem[-2],i,i+1,stem[-2]+1))
  for j in range(1,6):
   t=j/6;c=Vector((x+math.cos(a)*length*t,y+math.sin(a)*length*t,1.975+.23*math.sin(t*2)))
   for side in [-1,1]:
    d=Vector((math.cos(a+side*.9),math.sin(a+side*.9),.15))*.065*(1-t*.7);w=Vector((-d.y,d.x,0))*.20;i=len(verts);verts.extend([c,c+d*.45+w,c+d,c+d*.45-w]);faces.append((i,i+1,i+2,i+3))
 me=bpy.data.meshes.new('Pinnate fern');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Fern / fan '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(green);parent(o)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'luxembourg.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'luxembourg.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('LUXEMBOURG AUTHORED')
