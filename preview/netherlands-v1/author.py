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
ceramic=mat('Delft / ivory cobalt glaze',(.8,.8,.72),.3);maptex(ceramic,'delft-color.png','Base Color');maptex(ceramic,'delft-roughness.png','Roughness',True)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
blue=mat('Cobalt / seam',(.012,.035,.12),.32)
water=mat('Canal / deep blue',(.025,.16,.24),.23)
soil=mat('Dyke / clay',(.23,.20,.09),.85)
fields=[mat('Field / '+str(i),c,.82) for i,c in enumerate([(.20,.29,.085),(.34,.39,.14),(.41,.32,.12)])]
timber=mat('Mill / dark timber',(.07,.045,.025),.7)
sailmat=mat('Mill / ivory sails',(.71,.69,.54),.65)
exec((R/'helpers.py').read_text())
for o in list(bpy.data.objects):
 if o.type=='MESH' and not o.name.startswith('Studio') and not o.name.startswith(('Medallion','Side ring')):
  o.data.materials.clear();o.data.materials.append(blue if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Ceramic / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),ceramic,bevel=.025)
for sx in [-1,1]:cube('Ceramic / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),ceramic,bevel=.025,axis='Y')
cube('Ceramic / clasp seat',(0,-1.255,1.36),(.56,.075,.47),ceramic,bevel=.025)
for sy in [-1,1]:cube('Cobalt seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.08),blue,bevel=.009)
for sx in [-1,1]:
 cube('Cobalt seam / side',(sx*1.74,0,1.618),(.16,2.05,.08),blue,bevel=.009)
 for sy in [-1,1]:cube('Ceramic / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),ceramic,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),ceramic,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Ceramic / foot',(sx*1.47,sy*.91,-.10),(.48,.40,.32),blue,bevel=.06)
# Compact relief: water bed surrounds eight raised parcels, with open cross canals.
cube('Polder / water bed',(0,0,2.007),(2.75,1.60,.058),water,lid,.018)
for ix in range(4):
 for iy in range(2):
  x=-1.02+ix*.68;y=-.365+iy*.73
  cube('Polder / field '+str(ix)+' '+str(iy),(x,y,2.06),(.51,.53,.075),fields[(ix+iy)%3],lid,.013)
for sy in [-1,1]:cube('Polder / dyke long',(0,sy*.82,2.06),(2.88,.09,.13),soil,lid,.018)
for sx in [-1,1]:cube('Polder / dyke end',(sx*1.395,0,2.06),(.09,1.56,.13),soil,lid,.018)
# Small octagonal mill sits on rear/right field. Not a named building replica.
def cone(name,loc,r1,r2,depth,material):
 bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=r1,radius2=r2,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(material);parent(o);return o
cone('Mill / tower',(.91,.36,2.34),.17,.115,.49,timber)
cone('Mill / cap',(.91,.36,2.64),.18,0,.15,blue)
# Four separate broad latticed static sails arranged in X about a forward hub.
center=Vector((.91,.16,2.57))
for k in range(4):
 angle=math.pi/4+k*math.pi/2;d=Vector((math.cos(angle),0,math.sin(angle)))
 o=cube('Mill / sail '+str(k),center+d*.21,(.36,.025,.085),sailmat,bevel=.003);o.rotation_euler.y=-angle;parent(o)
 for j in range(4):
  q=center+d*(.08+j*.075);o=cube('Mill / sail rib',q+Vector((0,-.018,0)),(.013,.015,.11),timber,bevel=.002);o.rotation_euler.y=-angle;parent(o)
bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.055,location=center);o=bpy.context.object;o.name='Mill / hub';o.data.materials.append(gold);parent(o)

# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'netherlands.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'netherlands.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('NETHERLANDS AUTHORED')
