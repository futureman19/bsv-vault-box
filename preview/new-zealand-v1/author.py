"""Fiordland-inspired New Zealand pilot. Authored mesh and maps; no scans.
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
stone_mat=mat('Gneiss / cool mineral foliation',(.20,.25,.26),.65);maptex(stone_mat,'gneiss-color.png','Base Color');maptex(stone_mat,'gneiss-roughness.png','Roughness',True)
normal_tex=stone_mat.node_tree.nodes.new('ShaderNodeTexImage');normal_tex.image=bpy.data.images.load(str(R/'maps/gneiss-normal.png'));normal_tex.image.colorspace_settings.name='Non-Color';normal_tex.image.pack()
normal=stone_mat.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.3;stone_mat.node_tree.links.new(normal_tex.outputs['Color'],normal.inputs['Color']);stone_mat.node_tree.links.new(normal.outputs['Normal'],stone_mat.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
wood=stone_mat
end=stone_mat
granite=mat('Rock / pale exposed crags',(.26,.30,.29),.85);maptex(granite,'rock.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
moss=mat('Forest / wet slopes',(.035,.11,.065),.95)
seam=mat('Mineral seam / moss green',(.035,.07,.032),.9)
water=mat('Fiord / deep teal',(.018,.15,.17),.23,.12)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   co=o.matrix_world@co
   u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
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
# Continuous stone skins, not wooden finger courses.
for sy in [-1,1]:cube('Gneiss / front rear',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.015)
for sx in [-1,1]:cube('Gneiss / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.015)
# Small collar fills the central clasp mounting behind its retained position.
cube('Gneiss / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Gneiss / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
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
 for sy in [-1,1]:stone('Granite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Triangulated fiord and independent asymmetrical ridges.
def mesh(n,verts,faces,material):
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
N=40
ys=[-.85+1.7*i/N for i in range(N+1)]
def centre(y):return .16*math.sin(3*y)
def width(y):return .21+.025*math.cos(4*y)
v=[];f=[]
for y in ys:v.extend([(centre(y)-width(y),y,2.015),(centre(y)+width(y),y,2.015)])
for i in range(N):k=2*i;f.extend([(k,k+1,k+3),(k,k+3,k+2)])
mesh('Fiord / continuous water',v,f,water)
for side in [-1,1]:
 verts=[];faces=[]
 # Shore, lush steep face, exposed ridge, outer flank, lid-rooted perimeter.
 for i,y in enumerate(ys):
  wave=.055*math.sin(i*1.41+side)+.025*math.cos(i*2.7)
  envelope=math.sin(math.pi*i/N)**.6
  shore=centre(y)+side*width(y)
  peak=(.59 if side<0 else .73)*envelope+wave*envelope
  for x,z in [(shore,1.99),(shore+side*.17,2.01+peak*.64),(side*(.77+.05*math.sin(y*5)),1.99+peak),(side*(1.20+.08*math.cos(y*4)),1.99+peak*.35),(side*1.43,1.975)]:verts.append((x,y,z))
 for i in range(N):
  for j in range(4):
   a=5*i+j;b=a+5
   tris=[(a,a+1,b+1),(a,b+1,b)]
   if side<0:tris=[tuple(reversed(x)) for x in tris]
   faces.extend(tris)
 o=mesh('Ridge / '+('west' if side<0 else 'east'),verts,faces,moss);o.data.materials.append(granite)
 for poly in o.data.polygons:
  # Upper faces carry exposed stone, lower slopes remain deep green.
  j=(poly.index//2)%4
  poly.material_index=1 if j in [1,2] else 0
 # Open relief surfaces seat at outer edges in the lid; not watertight terrain solids.
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.0));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'new-zealand.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'new-zealand.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('NEW ZEALAND AUTHORED')
