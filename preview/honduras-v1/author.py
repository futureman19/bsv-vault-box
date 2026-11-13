"""Brief-led Honduras pilot. Authored mesh and maps; no photogrammetry.
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

stonebody=mat('Granite / weathered warm grey',(.3,.31,.26),.78)
maptex(stonebody,'stone-color.png','Base Color');maptex(stonebody,'stone-roughness.png','Roughness',True)
t=stonebody.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/stone-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();normal=stonebody.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.18;stonebody.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);stonebody.node_tree.links.new(normal.outputs['Normal'],stonebody.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
granite=stonebody
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
lidmat=mat('Lid / charcoal green satin',(.025,.055,.038),.32)
seam=mat('Seam / forest shadow',(.025,.045,.02),.9)
leafm=[mat('Rainforest / canopy '+str(i),c,.88) for i,c in enumerate([(.027,.09,.04),(.052,.14,.051),(.13,.23,.073)])]
water=mat('River / turquoise',(.018,.265,.30),.19,.12)
def uv(o,axis='X'):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(p.normal[i]));a,b=[i for i in range(3) if i!=axis]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(co[a]*.6+.5,co[b]*.6+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o

for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stonebody if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Granite / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stonebody,bevel=.025)
for sx in [-1,1]:cube('Granite / side wall',(sx*1.745,0,.83),(.23,2.10,1.46),stonebody,bevel=.025)
cube('Granite / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stonebody,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Granite / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stonebody,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),lidmat,lid,.045)
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
 for sy in [-1,1]:stone('Granite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)

# Winding river and banks share analytic edges; water center remains open.
def riverx(y):return .26*math.sin(4*y)+.12*y
N=65;ys=[-.94+i*1.88/(N-1) for i in range(N)]
def mesh(n,vs,fs,m):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(m);uv(o);parent(o);return o
vs=[]
for y in ys:
 x=riverx(y);vs.extend([(x-.105,y,2.013),(x+.105,y,2.013)])
mesh('River / continuous meander',vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(N-1)],water)
for sign in [-1,1]:
 vs=[]
 for y in ys:
  inner=riverx(y)+sign*.11
  for j in range(9):
   t=j/8;x=inner*(1-t)+sign*1.48*t;z=1.995+.10*math.sin(math.pi*t)+.18*max(0,y)*math.sin(math.pi*t)
   vs.append((x,y,z))
 fs=[]
 for i in range(N-1):
  for j in range(8):
   a=i*9+j;f=(a,a+1,a+10,a+9);fs.append(f if sign>0 else tuple(reversed(f)))
 # Close perimeter to lid surface: no floating paper-like bank edges.
 boundary=list(range(9))+[i*9+8 for i in range(1,N)]+list(range((N-1)*9+7,(N-1)*9-1,-1))+[i*9 for i in range(N-2,0,-1)]
 for k,a in enumerate(boundary):
  b=boundary[(k+1)%len(boundary)];c=len(vs);vs.extend([(vs[a][0],vs[a][1],1.978),(vs[b][0],vs[b][1],1.978)]);fs.append((a,b,c+1,c))
 mesh('Terrain / wooded bank '+str(sign),vs,fs,stonebody)
 for i in range(14):
  y=-.77+i*1.54/13;t=.35+.3*random.random();x=(riverx(y)+sign*.11)*(1-t)+sign*1.48*t
  ground=1.995+.10*math.sin(math.pi*t)+.18*max(0,y)*math.sin(math.pi*t)
  stone('Rainforest / trunk',(x,y,ground+.07),(.035,.035,.11),lid,stonebody,1)
  stone('Rainforest / canopy',(x,y,ground+.20),(.20,.13,.16),lid,leafm[i%3],2)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'honduras.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'honduras.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('HONDURAS AUTHORED')
