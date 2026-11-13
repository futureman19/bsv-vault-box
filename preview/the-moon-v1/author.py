"""Reference-led Japan pilot. Authored mesh and maps; no photogrammetry.
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
rock=mat('Regolith / neutral fractured gray',(.3,.3,.29),.88);maptex(rock,'regolith-color.png','Base Color');maptex(rock,'regolith-roughness.png','Roughness',True)
highland=mat('Highlands / pale impact breccia',(.48,.48,.45),.9);maptex(highland,'highland-color.png','Base Color');maptex(highland,'regolith-roughness.png','Roughness',True)
mare=mat('Mare / dark basalt',(.065,.075,.085),.86)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / charcoal',(.025,.03,.033),.95)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Rock projection')
 for p in o.data.polygons:
  axes=sorted(range(3),key=lambda i:abs(p.normal[i]))[:2]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]/2+.5,co[axes[1]]/2+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(rock if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Regolith / wall',(0,sy*1.145,.83),(3.72,.19,1.46),rock,bevel=.035)
for sx in [-1,1]:cube('Regolith / side',(sx*1.745,0,.83),(.23,2.10,1.46),rock,bevel=.035)
cube('Regolith / clasp seat',(0,-1.255,1.36),(.56,.075,.47),rock,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Regolith / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),rock,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),highland,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Regolith / foot',(sx*1.47,sy*.91,-.10),(.5,.44,.34),rock,bevel=.07)
# One continuous height field: bowls and ejecta rims are connected terrain,
# with no torus meshes, hidden planes or floating ornament bases.
craters=[(-.68,-.22,.52),(.65,.43,.255),(.85,-.55,.19)]
def height(x,y):
 z=2.055+.024*math.sin(x*4+y*2)+.016*math.cos(y*8-x*3)
 for cx,cy,r in craters:
  d=math.hypot(x-cx,y-cy)/r
  z+=.115*math.exp(-((d-1)/.19)**2)-.066*math.exp(-(d/.67)**4)
 return max(1.984,z)
verts=[];faces=[];nx=100;ny=66
for j in range(ny+1):
 for i in range(nx+1):
  x=-1.58+3.16*i/nx;y=-.94+1.88*j/ny
  # Blend perimeter down to the lid with an organic unraised boundary.
  e=min(1,(1.58-abs(x))/.13,(.94-abs(y))/.13)
  z=1.977+max(0,e)*(height(x,y)-1.977)
  verts.append((x,y,z))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
me=bpy.data.meshes.new('Continuous lunar impact surface');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / impact highlands',me);bpy.context.collection.objects.link(o);me.materials.append(highland);me.materials.append(mare)
surface=mat('Lunar terrain / highlands and mare',(.4,.4,.39),.9);maptex(surface,'terrain-color.png','Base Color');maptex(surface,'regolith-roughness.png','Roughness',True)
me.materials.clear();me.materials.append(surface)
for p in me.polygons:p.use_smooth=True
layer=me.uv_layers.new(name='Lunar plan')
for p in me.polygons:
 for li in p.loop_indices:
  v=me.vertices[me.loops[li].vertex_index].co;layer.data[li].uv=((v.x+1.58)/3.16,(v.y+.94)/1.88)
parent(o)
(R/'crater-spec.json').write_text(json.dumps({'craters':craters,'grid':[nx,ny]},indent=2))
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'the-moon.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'the-moon.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('THE MOON AUTHORED')
