"""Brief-led Palau pilot. Authored mesh and maps; no photogrammetry.
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
limestone=mat('Limestone / warm coralline',(.65,.61,.48),.78)
maptex(limestone,'limestone-color.png','Base Color');maptex(limestone,'limestone-roughness.png','Roughness',True)
water=mat('Lagoon / turquoise enamel',(.026,.34,.36),.23,.12)
maptex(water,'lagoon-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Lagoon / deep teal seam',(.016,.075,.07),.8)
forest=mat('Forest / evergreen crowns',(.07,.20,.085),.86)
maptex(forest,'forest-color.png','Base Color')
granite=limestone
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar UV')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   normal=p.normal
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u*.5+.5,v*.5+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(limestone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / front' if sy<0 else 'Limestone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),limestone,bevel=.025)
for sx in [-1,1]:cube('Limestone / side',(sx*1.745,0,.83),(.23,2.10,1.46),limestone,bevel=.025)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),limestone,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),limestone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),limestone,lid,.045)
cube('Lagoon / inset',(0,0,1.982),(3.30,1.95,.035),water,lid,.014)
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
 for sy in [-1,1]:stone('Limestone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Original ring-stack island profiles: undercut pale shoreline, wide forested crown.
# One connected closed triangulated surface per island, with material bands.
islands=[(-1.05,.38,.40,.29,.43),(-.22,.50,.34,.28,.53),(.66,.45,.43,.29,.58),(1.12,-.37,.28,.24,.34),(.24,-.40,.38,.25,.39),(-.72,-.43,.31,.21,.30)]
for k,(x,y,rx,ry,h) in enumerate(islands):
 verts=[];faces=[];N=28
 rings=[(0,.65),(.07,.73),(.19,1),(.42,.98),(.68,.80),(.88,.48)]
 for level,rad in rings:
  for j in range(N):
   a=j*math.tau/N;rough=1+.075*math.sin(a*3+k)+.045*math.cos(a*7+2*k)
   verts.append((x+rx*rad*rough*math.cos(a),y+ry*rad*rough*math.sin(a),1.987+h*level+.012*math.sin(a*4+k)*level))
 verts.extend([(x,y,1.987),(x+.02,y,1.987+h)])
 for r in range(len(rings)-1):
  for j in range(N):
   a=r*N+j;b=r*N+(j+1)%N;c=b+N;d=a+N
   faces.extend([(a,b,c),(a,c,d)])
 for j in range(N):faces.extend([(len(verts)-2,(j+1)%N,j),((len(rings)-1)*N+j,(len(rings)-1)*N+(j+1)%N,len(verts)-1)])
 me=bpy.data.meshes.new('Island triangulated terrain');me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new('Island / '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(limestone);me.materials.append(forest)
 for f in me.polygons:
  f.material_index=1 if f.center.z>1.987+h*.39 else 0
  f.use_smooth=True
 uv(o);parent(o)
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
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.7));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.9
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=900;scene.render.resolution_y=760;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'palau.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'palau.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PALAU AUTHORED')
