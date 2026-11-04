"""Twin Peaks & Narrows: original procedural landscape on inherited mechanism."""
import bpy, math, random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(869)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,f,socket,normal=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/f));t.image.pack()
 if socket!='Base Color':t.image.colorspace_settings.name='Non-Color'
 if normal:
  a=m.node_tree.nodes.new('ShaderNodeNormalMap');a.inputs['Strength'].default_value=.35;m.node_tree.links.new(t.outputs['Color'],a.inputs['Color']);m.node_tree.links.new(a.outputs['Normal'],m.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
 else:m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[socket])
rock=mat('Volcanic stone / charcoal pores',(.08,.09,.09),.8);tex(rock,'volcanic-color.png','Base Color');tex(rock,'volcanic-roughness.png','Roughness');tex(rock,'volcanic-normal.png','Normal',True)
gold=mat('Brass / satin gold',(.48,.30,.10),.28,.8)
inner=mat('Interior / dark mineral',(.045,.058,.055),.7)
sea=mat('Narrows / teal enamel',(.012,.24,.26),.23,.18)
shore=mat('Shoreline / pale sand',(.48,.43,.26),.84)
seam=mat('Seam / dark teal',(.018,.05,.046),.9)
forest=[mat('Forest / '+str(i),c,.89) for i,c in enumerate([(.024,.095,.033),(.043,.155,.052),(.074,.22,.073),(.12,.27,.095)])]
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar')
 for p in o.data.polygons:
  normal=p.normal;axis=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=axis]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(co[axes[0]]*.5+.5,co[axes[1]]*.5+.5)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Soft edges','BEVEL');mod.width=min(bevel,min(dim)*.35);mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(inner if o.name.startswith('Interior') else gold)
# Solid skins rather than cedar courses; original inner shell remains continuous.
for sy in [-1,1]:cube('Stone / front' if sy<0 else 'Stone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),rock,bevel=.025)
for sx in [-1,1]:cube('Stone / side',(sx*1.745,0,.83),(.23,2.10,1.46),rock,bevel=.025)
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),rock,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),rock,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),rock,lid,.045)
cube('Sea / inset',(0,0,1.988),(3.34,2.0,.024),sea,lid,.009)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone / foot',(sx*1.47,sy*.91,-.07),(.51,.44,.32),rock,bevel=.07)
# Radial ring meshes: true depressed crater and a separate forested cone.
# Both roots intersect the sea inset, no floating terrain. Footprints deliberately stylized.
def island(name,cx,cy,rx,ry,height,crater):
 N=72;K=24;verts=[(cx,cy,2.001+(height*.56 if crater else height))];faces=[];mats=[]
 for k in range(1,K+1):
  r=k/K
  for j in range(N):
   a=j*math.tau/N;coast=1+.055*math.sin(a*5+.3)+.035*math.cos(a*9)
   h=height*((1-r)**.72)
   if crater:h=height*(.56+.39*math.exp(-((r-.29)/.14)**2))*(1-r**2)**1.2
   h+=height*.038*math.sin(a*11+r*7)*math.sin(math.pi*r)
   verts.append((cx+rx*r*coast*math.cos(a),cy+ry*r*coast*math.sin(a),1.998+max(0,h)))
 for j in range(N):faces.append((0,1+j,1+(j+1)%N));mats.append(5 if crater else 3)
 for k in range(1,K):
  for j in range(N):
   a=1+(k-1)*N+j;b=1+(k-1)*N+(j+1)%N;c=1+k*N+(j+1)%N;d=1+k*N+j
   faces.extend([(a,b,c),(a,c,d)]);tone=max(0,min(3,int(1.6+1.1*math.sin(j*math.tau/N*3+k*.14)+.4*math.cos(j*math.tau/N*7-k*.3))));mi=0 if k>=K-1 else (5 if crater and k<8 else 1+tone);mats.extend([mi,mi])
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o)
 for m in [shore]+forest+[rock]:me.materials.append(m)
 for p,mi in zip(me.polygons,mats):p.material_index=mi;p.use_smooth=True
 uv(o);parent(o);return o
island('Terrain / Saint Kitts crater',-.71,.19,.74,.66,.77,True)
island('Terrain / Nevis peak',.88,-.22,.51,.49,.70,False)
# Rimmed gold medallion, a family embellishment, not a national symbol.
bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.13,depth=.035,location=(0,-1.258,.87),rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / solid emblem';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.24
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.2));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.25))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=760;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'saint-kitts-and-nevis.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'saint-kitts-and-nevis.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('AUTHOR PASS: Twin Peaks & Narrows')
