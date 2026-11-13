"""Brief-driven Bhutan pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Timber / dark fine grain',(.1,.045,.025),.55);maptex(wood,'timber-color.png','Base Color');maptex(wood,'timber-roughness.png','Roughness',True)
plaster=mat('Earth / warm chalk plaster',(.61,.49,.30),.87);maptex(plaster,'plaster-color.png','Base Color')
red=mat('Paint / oxblood',(.178,.027,.020),.56)
teal=mat('Paint / subdued teal',(.041,.162,.145),.56)
ochre=mat('Paint / golden ochre',(.552,.323,.067),.60)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
granite=mat('Stone / mountain grey',(.18,.21,.20),.88);maptex(granite,'stone-color.png','Base Color')
seam=mat('Seam / dark umber',(.025,.018,.012),.95)
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
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Four thick skins, with independent continuous inherited interior behind them.
for sy in [-1,1]:cube('Earth / body long',(0,sy*1.145,.83),(3.72,.19,1.46),plaster,bevel=.015)
for sx in [-1,1]:cube('Earth / body side',(sx*1.745,0,.83),(.23,2.10,1.46),plaster,bevel=.015,axis='Y')
cube('Timber / clasp seat',(0,-1.255,1.36),(.56,.075,.47),red,bevel=.025)
# Deliberately sparse timber frames leave broad pale-earth fields readable.
for sy in [-1,1]:
 for x in [-1.68,-.91,.91,1.68]:cube('Timber / upright',(x,sy*1.247,.86),(.075,.025,1.22),red,bevel=.005)
 for z in [.25,1.47]:cube('Timber / cross rail',(0,sy*1.247,z),(3.40,.025,.075),red,bevel=.005)
for sx in [-1,1]:
 for y in [-.91,.91]:cube('Timber / side upright',(sx*1.872,y,.86),(.025,.075,1.22),red,bevel=.005)
 for z in [.25,1.47]:cube('Timber / side rail',(sx*1.872,0,z),(.025,1.90,.075),red,bevel=.005)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Timber / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),red,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
# Stepped red timber cornice on the moving lid, not the body seam.
for sy in [-1,1]:
 cube('Cornice / long',(0,sy*1.11,2.015),(3.5,.12,.065),red,lid,.009)
 cube('Cornice / ochre long',(0,sy*1.11,2.055),(3.5,.08,.025),ochre,lid,.004)
for sx in [-1,1]:
 cube('Cornice / side',(sx*1.70,0,2.015),(.12,2.10,.065),red,lid,.009)
 cube('Cornice / ochre side',(sx*1.70,0,2.055),(.08,2.10,.025),ochre,lid,.004)
for sy in [-1,1]:
 for j in range(15):
  x=-1.48+j*.211
  cube('Painted border / teal inset',(x,sy*.91,1.99),(.12,.12,.023),teal,lid,.004)
  o=cube('Painted border / ochre diamond',(x,sy*.91,2.009),(.054,.054,.014),ochre,lid,.002);o.rotation_euler.z=math.pi/4
for sx in [-1,1]:
 for j in range(7):cube('Painted border / side inset',(sx*1.48,-.65+j*.216,1.99),(.12,.12,.023),teal,lid,.004)
def stone(n,loc,scale,p=None,material=granite,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Stone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
# A continuous irregular low mountain relief, with no named/sacred landmark claim.
verts=[];faces=[];nx=30;ny=16
for j in range(ny+1):
 y=-.5+j/ny
 for i in range(nx+1):
  x=-1.1+2.2*i/nx
  edge=math.sin(math.pi*i/nx)*math.sin(math.pi*j/ny)
  peaks=max(.42*math.exp(-((x+.50)**2/.055+(y-.08)**2/.10)),.55*math.exp(-((x-.02)**2/.07+(y+.03)**2/.09)),.34*math.exp(-((x-.63)**2/.08+(y-.05)**2/.08)))
  z=1.982+edge*(.025+peaks+random.uniform(-.016,.016))
  verts.append((x,y,z))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.extend([(a,a+1,a+nx+2),(a,a+nx+2,a+nx+1)])
me=bpy.data.meshes.new('Mountain relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Mountain / asymmetric relief',me);bpy.context.collection.objects.link(o);me.materials.append(granite);uv(o);parent(o)
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'bhutan.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'bhutan.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('BHUTAN AUTHORED')
