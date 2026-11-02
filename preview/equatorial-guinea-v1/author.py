"""Bioko landscape synthesis, original script-authored geometry.
Reuses only Japan's trimmed mechanism, not its cedar artwork. Run maps.py first.
"""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(224004)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,file,input,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();p=m.node_tree.nodes.get('Principled BSDF')
 if input=='Normal':
  n=m.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.5;m.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);m.node_tree.links.new(n.outputs['Normal'],p.inputs[input])
 else:m.node_tree.links.new(t.outputs['Color'],p.inputs[input])
basalt=mat('Basalt / weathered charcoal',(.06,.06,.055),.75)
for file,input,nc in [('basalt-color.png','Base Color',False),('basalt-roughness.png','Roughness',True),('basalt-normal.png','Normal',True)]:tex(basalt,file,input,nc)
polished=mat('Basalt / satin lid',(.025,.033,.029),.32)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
liner=mat('Interior / dark mineral',(.035,.042,.034),.65)
seam=mat('Seam / forest green',(.035,.07,.032),.9)
forest=[mat('Canopy / '+str(i),c,.9) for i,c in enumerate([(.022,.085,.032),(.043,.14,.046),(.075,.20,.066)])]
terrainmat=mat('Terrain / deep green basalt',(.035,.075,.038),.85)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Portable mineral UV')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o)
 if bevel:
  m=o.modifiers.new('Soft edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
# Continuous baseline liner remains behind narrow segmented exterior skins.
for sy in [-1,1]:
 for i in range(4):cube('Basalt / long panel',(-1.395+i*.93,sy*1.145,.83),(.928,.19,1.46),basalt,bevel=.014)
for sx in [-1,1]:
 cube('Basalt / side panel',(sx*1.745,0,.83),(.23,2.10,1.46),basalt,bevel=.018)
cube('Basalt / clasp seat',(0,-1.255,1.36),(.56,.075,.47),basalt,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Basalt / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),basalt,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),polished,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def stone(n,loc,scale,material,p=None,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.09,.09);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for f in o.data.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Basalt foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),basalt,sub=3)
# An irregular radial height field: depressed western caldera, broader eastern shield.
# Boundary tapers down to the lid; no rectangular display plinth.
def relief(x,y):
 r=math.sqrt(((x+.35)/.53)**2+((y-.10)/.42)**2)
 rim=.30*math.exp(-((r-.92)/.25)**2)
 shield=.32*math.exp(-(((x-.48)/.66)**2+((y-.12)/.50)**2)*1.8)
 detail=.018*math.sin(x*21+y*13)*math.sin(y*17-x*7)
 return 2.005+rim+shield+detail
verts=[(-.12,.08,relief(-.12,.08))];faces=[];rings=24;sides=96
for i in range(1,rings+1):
 r=i/rings
 for j in range(sides):
  a=j*math.tau/sides;edge=1+.04*math.sin(5*a)+.025*math.cos(9*a);x=-.12+1.32*r*math.cos(a)*edge;y=.08+.80*r*math.sin(a)*edge
  z=1.975+(relief(x,y)-1.975)*min(1,(1-r)*8)
  verts.append((x,y,z))
for j in range(sides):faces.append((0,1+j,1+(j+1)%sides))
for i in range(rings-1):
 for j in range(sides):
  a=1+i*sides+j;b=1+i*sides+(j+1)%sides;c=b+sides;d=a+sides;faces.extend([(a,b,c),(a,c,d)])
me=bpy.data.meshes.new('Bioko shield relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / shield and caldera',me);bpy.context.collection.objects.link(o);me.materials.append(terrainmat);parent(o)
for f in me.polygons:f.use_smooth=True
# Forest crowns lie on shoulders, not in the depressed crater. Flattened broadleaf forms.
count=0
while count<72:
 x=random.uniform(-1.25,1.05);y=random.uniform(-.61,.75)
 r=math.sqrt(((x+.35)/.53)**2+((y-.10)/.42)**2)
 if ((x+.12)/1.22)**2+((y-.08)/.70)**2>1 or r<1.12:continue
 z=relief(x,y);s=random.uniform(.09,.16)
 stone('Canopy / crown '+str(count),(x,y,z+.035),(s,s*.8,s*.52),forest[count%3],lid,2);count+=1
# Thin brass inset line around the body is fictional collection detailing.
for sy in [-1,1]:cube('Brass / lower edge',(0,sy*1.242,.22),(3.40,.012,.022),gold,bevel=.003)
for sx in [-1,1]:cube('Brass / side lower edge',(sx*1.864,0,.22),(.012,2.10,.022),gold,bevel=.003)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.3));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'equatorial-guinea.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'equatorial-guinea.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PASS EQUATORIAL GUINEA AUTHORED')
