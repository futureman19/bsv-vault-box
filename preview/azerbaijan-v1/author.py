import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'helpers.py').read_text())
copper=mat('Lahij / hammered copper',(.39,.11,.045),.4,.78)
maptex(copper,'copper-color.png','Base Color');maptex(copper,'copper-roughness.png','Roughness',True)
t=copper.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/copper-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();normal=copper.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.4;copper.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);copper.node_tree.links.new(normal.outputs['Normal'],copper.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / satin fittings',(.48,.30,.10),.28,.8)
seam=mat('Umber / seam',(.035,.018,.012),.9)
liner=mat('Interior / dark copper',(.13,.045,.023),.65,.55)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Copper / front' if sy<0 else 'Copper / rear',(0,sy*1.145,.83),(3.26,.19,1.46),copper,bevel=.016)
for sx in [-1,1]:cube('Copper / side',(sx*1.745,0,.83),(.23,2.38,1.46),copper,bevel=.016)
cube('Copper / clasp seat',(0,-1.255,1.36),(.56,.075,.47),copper,bevel=.025)
for sy in [-1,1]:cube('Umber seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Umber seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Copper / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),copper,bevel=.004)
  cube('Brass foot',(sx*1.47,sy*.91,-.08),(.48,.40,.30),gold,bevel=.05)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),copper,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def disk(n,r,z,depth,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=r,depth=depth,location=(0,0,z));o=bpy.context.object;o.name=n;o.data.materials.append(material);uv(o);parent(o);return o
disk('Ornament / medallion',.76,1.998,.04,copper)
for r in [.69,.75]:
 bpy.ops.mesh.primitive_torus_add(major_segments=96,minor_segments=8,major_radius=r,minor_radius=.009,location=(0,0,2.023));o=bpy.context.object;o.name='Ornament / ring';o.data.materials.append(gold);parent(o)
for k in range(8):
 a=k*math.tau/8;verts=[]
 # pointed raised leaves, radial separation and closed underside
 for z in [2.019,2.052]:
  for along,across in [(0,0),(.18,.08),(.37,0),(.18,-.08)]:
   r=.20+along;verts.append((math.cos(a)*r-math.sin(a)*across,math.sin(a)*r+math.cos(a)*across,z))
 faces=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 me=bpy.data.meshes.new('leaf');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Ornament / leaf '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(gold);parent(o)
disk('Ornament / center',.09,2.038,.04,gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.24
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.8));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'azerbaijan.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'azerbaijan.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('AZERBAIJAN AUTHORED')
