"""Spain original ceramic-inspired collectible. Run maps.py first."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'helpers.py').read_text())
# Face-normal UV projection avoids stretched stone/ceramic side grain.
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Ceramic projection')
 for f in o.data.polygons:
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(f.normal.z)>.7:u,v=co.x,co.y
   elif abs(f.normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/1.3+.5,v/1.3+.5)
clay=mat('Terracotta / fired clay',(.47,.115,.047),.55);maptex(clay,'clay-color.png','Base Color');maptex(clay,'glaze-roughness.png','Roughness',True)
ivory=mat('Ivory / satin glaze',(.855,.745,.52),.3);maptex(ivory,'ivory-color.png','Base Color');maptex(ivory,'glaze-roughness.png','Roughness',True)
pattern=mat('Ceramic / original cobalt petals',(.855,.745,.52),.3);maptex(pattern,'ceramic-pattern.png','Base Color');maptex(pattern,'glaze-roughness.png','Roughness',True)
cobalt=mat('Cobalt / blue glaze',(.015,.064,.266),.24)
ochre=mat('Ochre / honey glaze',(.558,.283,.037),.32)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / midnight blue',(.009,.018,.035),.85)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(ivory if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:
 cube('Clay / front' if sy<0 else 'Clay / rear',(0,sy*1.145,.83),(3.72,.19,1.46),clay,bevel=.016)
 # Glazed inset field sitting just proud of clay; below seam and latch bearings.
 cube('Glaze panel / front' if sy<0 else 'Glaze panel / rear',(0,sy*1.246,.82),(3.24,.014,1.12),pattern,bevel=.003)
for sx in [-1,1]:
 cube('Clay / side',(sx*1.745,0,.83),(.23,2.10,1.46),clay,bevel=.016)
 cube('Glaze panel / side',(sx*1.868,0,.82),(.014,1.94,1.12),pattern,bevel=.003)
cube('Clay / clasp seat',(0,-1.275,1.36),(.56,.075,.47),clay,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Clay / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),clay,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),clay,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Clay foot',(sx*1.47,sy*.91,-.08),(.49,.43,.31),clay,bevel=.065)
# Raised perimeter tiles and central low-relief rosette.
for sy in [-1,1]:
 for i in range(11):cube('Lid ornament / border',(i*.28-1.4,sy*.94,1.997),(.255,.21,.038),cobalt if i%2 else ivory,lid,.008)
for sx in [-1,1]:
 for i in range(5):cube('Lid ornament / border',(sx*1.49,(i-2)*.29,1.997),(.21,.255,.038),ivory if i%2 else cobalt,lid,.008)
def disk(n,loc,r,depth,m,p=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m);uv(o)
 mod=o.modifiers.new('Ceramic edge','BEVEL');mod.width=min(.008,depth*.3);mod.segments=2;select(o);bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
disk('Lid ornament / ivory medallion',(0,0,2.011),.78,.065,ivory,lid)
for i in range(8):
 a=i*math.tau/8;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0))
 points=[u*.16,u*.42+v*.13,u*.69,u*.42-v*.13];verts=[(q.x,q.y,z) for z in [2.043,2.077] for q in points]
 faces=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 me=bpy.data.meshes.new('Pointed ceramic petal');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Lid ornament / cobalt petal',me);bpy.context.collection.objects.link(o);me.materials.append(cobalt);parent(o)
 disk('Lid ornament / ochre bead',(.86*math.cos(a),.72*math.sin(a),2.006),.038,.048,ochre,lid)
disk('Lid ornament / ochre center',(0,0,2.067),.12,.046,ochre,lid)
# Clean unused resources; render exact source, not promotional imagery.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.25
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.7));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.65
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=1000;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'spain.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'spain.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('SPAIN AUTHORED')
