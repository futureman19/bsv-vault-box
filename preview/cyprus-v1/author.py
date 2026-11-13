"""Brief-led Cyprus pilot. Authored mesh and maps; no photogrammetry.
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
   if abs(p.normal.z)>.7: u,v=co.x,co.y
   elif abs(p.normal.x)>.7: u,v=co.y,co.z
   else: u,v=co.x,co.z
   layer.data[li].uv=(u/2+.5,v/2+.5)

def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o

linen=mat('Linen / warm woven brown',(.24,.12,.055),.8)
maptex(linen,'linen-color.png','Base Color');maptex(linen,'linen-roughness.png','Roughness',True)
t=linen.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/linen-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=linen.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.35;linen.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);linen.node_tree.links.new(n.outputs['Normal'],linen.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
beige=mat('Linen / ecru binding',(.52,.37,.22),.75)
ivory=mat('Cotton / ivory thread',(.88,.79,.61),.82)
dark=mat('Linen / brown inset',(.10,.038,.012),.9)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(linen if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Linen body / front-rear',(0,sy*1.145,.83),(3.26,.19,1.46),linen,bevel=.02)
for sx in [-1,1]:cube('Linen body / side',(sx*1.745,0,.83),(.23,2.48,1.46),linen,bevel=.02)
cube('Linen / clasp seat',(0,-1.255,1.36),(.56,.075,.47),linen,bevel=.025)
for sy in [-1,1]:cube('Binding seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),beige,bevel=.009)
for sx in [-1,1]:
 cube('Binding seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),beige,bevel=.009)
 for sy in [-1,1]:cube('Binding / corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),beige,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),beige,lid,.045)
cube('Cutwork / inset carrier',(0,0,1.99175),(3.20,1.86,.0285),dark,lid,.01)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Linen / foot',(sx*1.47,sy*.91,-.10),(.52,.45,.32),dark,bevel=.06)
def tube(n,points,radii,material,p=lid,sides=9):
 verts=[];faces=[]
 for i,c in enumerate(points):
  c=Vector(c);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.normalize();a=t.cross(Vector((0,1,0)))
  if a.length<.01:a=t.cross(Vector((1,0,0)))
  a.normalize();b=t.cross(a).normalized()
  for j in range(sides):verts.append(c+radii[i]*(a*math.cos(j*math.tau/sides)+b*math.sin(j*math.tau/sides)))
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;bb=i*sides+(j+1)%sides;faces.append((a,bb,bb+sides,a+sides))
 faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))]);me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material)
 for f in me.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o

# Six invented diamond cutwork motifs; apertures expose carrier, not hollow box.
for ix,x in enumerate([-1.02,0,1.02]):
 for iy,y in enumerate([-.43,.43]):
  for label,rx,ry,r in [('outer',.43,.34,.023),('inner',.20,.15,.023)]:
   pts=[(x+rx,y,2.028),(x,y+ry,2.028),(x-rx,y,2.028),(x,y-ry,2.028),(x+rx,y,2.028)]
   tube(f'Cutwork diamond {ix}-{iy} / {label}',pts,[r]*5,ivory,sides=8)
# Even hemstitch-inspired border: all stitch ends rooted in dark carrier.
for i in range(35):
 x=-1.48+i*2.96/34
 for sy in [-1,1]:cube('Cutwork / border stitch',(x,sy*.845,2.015),(.020,.12,.030),ivory,lid,.004)
for i in range(16):
 y=-.72+i*1.44/15
 for sx in [-1,1]:cube('Cutwork / side stitch',(sx*1.52,y,2.015),(.12,.020,.030),ivory,lid,.004)
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'cyprus.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'cyprus.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('CYPRUS AUTHORED')
