"""Cameroon landscape pilot. Authored mesh and maps; no photogrammetry.
Run maps.py first. Reproduction uses only the included trimmed mechanism.blend.
"""
import bpy,bmesh,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(237)
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
basalt=mat('Basalt / warm volcanic stone',(.10,.075,.055),.82);maptex(basalt,'basalt-color.png','Base Color');maptex(basalt,'basalt-roughness.png','Roughness',True)
t=basalt.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/basalt-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=basalt.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.3;basalt.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);basalt.node_tree.links.new(n.outputs['Normal'],basalt.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
granite=basalt
gold=mat('Brass / aged satin',(.40,.24,.075),.32,.8)
seam=mat('Seam / charcoal gasket',(.022,.026,.018),.95)
forest=[mat('Rainforest / '+str(i),c,.93) for i,c in enumerate([(.026,.065,.032),(.045,.095,.039),(.075,.13,.048)])]
grass=mat('Grassland / upper slopes',(.12,.145,.062),.95)
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
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(basalt if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Continuous dressed volcanic stone walls, not stacked timber or columns.
for sy in [-1,1]:cube('Basalt / front' if sy<0 else 'Basalt / rear',(0,sy*1.145,.83),(3.72,.19,1.46),basalt,bevel=.045)
for sx in [-1,1]:cube('Basalt / side',(sx*1.745,0,.83),(.23,2.10,1.46),basalt,bevel=.035,axis='Y')
cube('Basalt / clasp seat',(0,-1.255,1.36),(.56,.075,.47),basalt,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Basalt / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),basalt,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),basalt,lid,.045)
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
 for sy in [-1,1]:stone('Basalt foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
# Continuous irregular elliptical massif with multiple asymmetric cinder shoulders.
def height(x,y):
 r=math.sqrt((x/1.40)**2+((y-.05)/.82)**2)
 envelope=max(0,1-r*r)**1.3
 peaks=.48*math.exp(-((x-.27)/.52)**2-((y-.20)/.40)**2)+.25*math.exp(-((x+.62)/.28)**2-((y+.03)/.26)**2)+.23*math.exp(-((x-.78)/.24)**2-((y+.15)/.26)**2)
 ridges=.035*math.sin(x*18+y*11)+.023*math.sin(x*31-y*19)
 return 1.985+envelope*(.12+peaks+ridges)
verts=[(0,.05,height(0,.05))];faces=[];rings=20;segments=80
for i in range(1,rings+1):
 r=i/rings
 for j in range(segments):
  a=j*math.tau/segments;ir=r*(1+.035*math.sin(a*7)+.025*math.sin(a*11));x=1.36*ir*math.cos(a);y=.05+.78*ir*math.sin(a);verts.append((x,y,height(x,y)))
for j in range(segments):faces.append((0,1+j,1+(j+1)%segments))
for i in range(rings-1):
 for j in range(segments):
  a=1+i*segments+j;b=1+i*segments+(j+1)%segments;c=b+segments;d=a+segments;faces.extend([(a,d,c),(a,c,b)])
# Close underside inside slab; do not leave relief as a floating open sheet.
verts.append((0,.05,1.975));bottom=len(verts)-1
for j in range(segments):faces.append((bottom,1+(rings-1)*segments+(j+1)%segments,1+(rings-1)*segments+j))
me=bpy.data.meshes.new('Fako relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Fako / elongated volcanic massif',me);bpy.context.collection.objects.link(o);me.materials.append(basalt);me.materials.append(grass);uv(o)
for f in me.polygons:
 f.material_index=1 if 2.06<f.center.z<2.22 else 0
parent(o)
# Low canopy clusters seated in lower slopes; no summit trees or hinge obstructions.
for i in range(100):
 a=random.uniform(0,math.tau);r=random.uniform(.61,.91);x=1.32*r*math.cos(a);y=.05+.73*r*math.sin(a);z=height(x,y)
 stone('Rainforest / lower flank canopy',(x,y,z+.025),(.09+random.random()*.04,.07+random.random()*.035,.045+random.random()*.025),lid,forest[i%3],2)
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'cameroon.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'cameroon.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('CAMEROON AUTHORED')
