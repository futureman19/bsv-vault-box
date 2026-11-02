"""Original Kyrgyz craft-inspired chest. Reuses only the frozen family mechanism."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'geometry.py').read_text())
wood=mat('Walnut / dark frame',(.075,.032,.019),.55)
felt=mat('Felt / crimson wool',(.27,.019,.038),.9)
maptex(felt,'felt-color.png','Base Color');maptex(felt,'felt-roughness.png','Roughness',True)
t=felt.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/felt-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();normal=felt.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.25;felt.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);felt.node_tree.links.new(normal.outputs['Normal'],felt.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
ivory=mat('Felt / ivory applique',(.82,.69,.47),.92)
gold=mat('Brass / antique satin',(.48,.30,.10),.3,.8)
seam=mat('Seam / dark felt',(.024,.009,.012),.98)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
for sy in [-1,1]:
 cube('Frame / long',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.018)
 cube('Felt panel / front' if sy<0 else 'Felt panel / rear',(0,sy*1.247,.83),(3.33,.028,1.12),felt,bevel=.009)
 # seam is recessed on rear to clear hinge leaves
 cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.617),(3.28,.08,.085),seam,bevel=.008)
for sx in [-1,1]:
 cube('Frame / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.015)
 cube('Felt panel / side',(sx*1.868,0,.83),(.025,1.99,1.12),felt,bevel=.008,axis='Y')
 cube('Seam / side',(sx*1.74,0,1.617),(.16,2.05,.085),seam,bevel=.008)
 for sy in [-1,1]:
  cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
  cube('Foot / walnut',(sx*1.48,sy*.91,-.04),(.38,.35,.28),wood,bevel=.06)
  cube('Foot / brass shoe',(sx*1.48,sy*.91,-.16),(.39,.36,.06),gold,bevel=.02)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
cube('Felt lid / inset',(0,0,1.991),(3.30,1.97,.035),felt,lid,.012)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Low-relief closed tubes create tangible applique, not a painted motif.
def cord(name,points,rad,material,p=None,flatten=1):
 vs=[];faces=[];sides=8
 for i,c in enumerate(points):
  c=Vector(c);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)]);t.normalize();a=t.cross(Vector((0,0,1)))
  if a.length<.01:a=t.cross(Vector((0,1,0)))
  a.normalize();b=t.cross(a).normalized()
  for j in range(sides):vs.append(c+rad*(a*math.cos(j*math.tau/sides)+b*math.sin(j*math.tau/sides)*flatten))
 for i in range(len(points)-1):
  for j in range(sides):k=i*sides+j;l=i*sides+(j+1)%sides;faces.append((k,l,l+sides,k+sides))
 faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))])
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material)
 for f in me.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
# Four mirrored pairs of inward curling ivory horns, symmetric field around medallion.
for cx in [-1.03,1.03]:
 for cy in [-.47,.47]:
  for side in [-1,1]:
   pts=[]
   for i in range(37):
    t=i/36;ang=-math.pi/2+t*math.pi*1.85;r=.29*(1-.76*t)
    pts.append((cx+side*(.10+r*math.cos(ang)),cy+r*math.sin(ang),2.023))
   cord('Shyrdak / lid horn',pts,.042,ivory,lid,.43)
# Two mirrored pairs on front and rear, avoiding the inherited central latch.
for sy in [-1,1]:
 for cx in [-1.03,1.03]:
  for side in [-1,1]:
   pts=[]
   for i in range(33):
    t=i/32;ang=-math.pi/2+t*math.pi*1.85;r=.28*(1-.76*t)
    pts.append((cx+side*(.10+r*math.cos(ang)),sy*1.28,.83+r*math.sin(ang)))
   cord('Shyrdak / wall horn',pts,.028,ivory)
# Geometric diamond and central paired curls, no asserted traditional symbolism.
cord('Shyrdak / medallion',[(0,-.49,2.020),(.45,0,2.020),(0,.49,2.020),(-.45,0,2.020),(0,-.49,2.020)],.025,ivory,lid,.55)
for side in [-1,1]:
 pts=[]
 for i in range(29):
  t=i/28;a=-math.pi/2+t*math.pi*1.8;r=.16*(1-.7*t);pts.append((side*(.08+r*math.cos(a)),r*math.sin(a),2.020))
 cord('Shyrdak / center curl',pts,.024,gold,lid,.55)
# Individually modeled running stitches: two long rows and two short rows.
for sy in [-1,1]:
 for i in range(40):cube('Stitch / lid long',(-1.53+i*3.06/39,sy*.92,2.012),(.034,.014,.012),ivory,lid,0)
for sx in [-1,1]:
 for i in range(23):cube('Stitch / lid short',(sx*1.58,-.83+i*1.66/22,2.012),(.014,.034,.012),ivory,lid,0)
for sy in [-1,1]:
 for z in [.32,1.34]:
  for i in range(37):
   x=-1.53+i*3.06/36
   if abs(x)<.32:continue
   cube('Stitch / wall',(x,sy*1.266,z),(.037,.012,.014),ivory,bevel=0)
# Batch the disconnected stitch islands per rigid owner to reduce draw calls.
for moving in [False,True]:
 objs=[o for o in bpy.data.objects if o.name.startswith('Stitch /') and bool(o.parent)==moving]
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();bpy.context.object.name='Stitches / lid' if moving else 'Stitches / wall'
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.20
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.6));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.05))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'kyrgyzstan.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'kyrgyzstan.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('KYRGYZSTAN AUTHORED')
