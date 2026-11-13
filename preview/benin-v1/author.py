"""Benin / Atakora Earth. Original procedural geometry on frozen family mechanism."""
import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(1140)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.preferences.filepaths.save_version=0
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();m=o.matrix_world.copy();o.parent=p;o.matrix_world=m;return o
def mat(n,c,r=.85,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,file,socket,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[socket])
earth=mat('Earth / warm hand-smoothed plaster',(.34,.12,.045));tex(earth,'earth-color.png','Base Color');tex(earth,'earth-roughness.png','Roughness',True)
straw=mat('Straw / dry woven gold',(.42,.25,.07),.9);tex(straw,'straw-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
um=mat('Umber / seam and recess',(.045,.018,.008),.92)
liner=mat('Interior / dark earthen liner',(.19,.065,.025),.88)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Plaster planar')
 for f in o.data.polygons:
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if abs(f.normal.x)>.7 else co.x;v=co.y if abs(f.normal.z)>.7 else co.z
   layer.data[li].uv=(u/1.9+.5,v/1.6+.5)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Soft plaster edges','BEVEL');mod.width=min(bevel,min(dim)*.35);mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
def cone(n,loc,r1,r2,depth,m,p=None,vertices=40):
 bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=r1,radius2=r2,depth=depth,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
# Wide continuous skins; irregular compact maps, no geological stripes.
for sy in [-1,1]:cube('Earth body / front' if sy<0 else 'Earth body / rear',(0,sy*1.145,.83),(3.72,.19,1.46),earth,bevel=.045)
for sx in [-1,1]:cube('Earth body / side',(sx*1.745,0,.83),(.23,2.10,1.46),earth,bevel=.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Earth / rounded buttress',(sx*1.70,sy*1.09,.82),(.34,.34,1.48),earth,bevel=.11)
  cube('Earth / foot',(sx*1.47,sy*.91,-.08),(.48,.43,.32),earth,bevel=.10)
cube('Earth / clasp seat',(0,-1.255,1.36),(.56,.075,.47),earth,bevel=.025)
for sy in [-1,1]:cube('Umber seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),um,bevel=.009)
for sx in [-1,1]:
 cube('Umber seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),um,bevel=.009)
 for sy in [-1,1]:cube('Earth / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),earth,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),earth,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Stylized joined-tower compound: low walls/terrace join three tapered towers.
# Every architectural surface is a direct lid child, so whole ornament travels.
cube('Takienta / terrace',(0,.12,2.01),(2.10,1.12,.11),earth,lid,.05)
for x in [-.78,.78]:
 cone('Takienta / tower roofed', (x,.32,2.24),.27,.235,.52,earth,lid)
 cone('Takienta / thatched roof',(x,.32,2.63),.34,.025,.30,straw,lid)
 # Roof sloping ridges are solid tapered rods, original straw-like relief.
 for j in range(20):
  a=j*math.tau/20;start=Vector((x+.325*math.cos(a),.32+.325*math.sin(a),2.49));end=Vector((x+.03*math.cos(a),.32+.03*math.sin(a),2.772));d=end-start
  o=cone('Takienta / roof rib',(start+end)/2,.009,.004,d.length,straw,None,8);o.rotation_euler=d.to_track_quat('Z','Y').to_euler();parent(o)
cone('Takienta / tower flat',(0,-.27,2.22),.29,.26,.46,earth,lid)
cone('Takienta / recessed roof',(0,-.27,2.455),.207,.207,.012,um,lid)
# Parapet ring uses a true open aperture, not a solid disc.
bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=10,major_radius=.236,minor_radius=.028,location=(0,-.27,2.472));o=bpy.context.object;o.name='Takienta / parapet';o.data.materials.append(earth);parent(o)
for x in [-.39,.39]:cube('Takienta / joining wall',(x,.22,2.23),(.50,.17,.42),earth,lid,.035)
# Deliberate relief doorway, not a claim of a fully modelled interior.
cube('Takienta / doorway',(0,-.548,2.16),(.13,.016,.22),um,lid,.035)
# Restrained solid disc, no copied cultural or royal symbol.
cone('Medallion / solid emblem',(0,-1.258,.87),.13,.13,.035,gold).rotation_euler.x=math.pi/2
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.25
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.2));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.20))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'benin.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'benin.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('BENIN AUTHORED')
