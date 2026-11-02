"""Blender-authored Pearl & Coral Stone; original geometric interpretation."""
import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(1364)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.preferences.filepaths.save_version=0
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def texture(m,file,socket,normal=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True);t.image.pack()
 if socket!='Base Color':t.image.colorspace_settings.name='Non-Color'
 out=t.outputs['Color']
 if normal:
  nm=m.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.45;m.node_tree.links.new(out,nm.inputs['Color']);out=nm.outputs['Normal']
 m.node_tree.links.new(out,m.node_tree.nodes.get('Principled BSDF').inputs[socket])
stone=mat('Coral stone / warm porous cream',(.56,.45,.28),.75)
texture(stone,'stone-color.png','Base Color');texture(stone,'stone-roughness.png','Roughness');texture(stone,'stone-normal.png','Normal',True)
gold=mat('Brass / aged satin',(.48,.30,.10),.28,.8)
teal=mat('Lagoon / deep teal enamel',(.021,.15,.162),.26,.15)
seam=mat('Seam / dark teal',(.012,.036,.038),.8)
nacre=mat('Shell / warm nacre',(.72,.64,.49),.30,.12)
pearl=mat('Pearl / ivory lustre',(.88,.84,.73),.16,.12)
liner=mat('Interior / warm limestone',(.37,.30,.21),.75)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar')
 for p in o.data.polygons:
  ax=max(range(3),key=lambda i:abs(p.normal[i]));axes=[i for i in range(3) if i!=ax]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(co[axes[0]]/2+.5,co[axes[1]]/2+.5)
def cube(n,loc,dim,material,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o)
 if bevel:
  m=o.modifiers.new('Soft edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
# Continuous outer stone skins; no wood courses, fingers, tree or borrowed landscape.
for sy in [-1,1]:cube('Stone / front' if sy<0 else 'Stone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.035)
for sx in [-1,1]:cube('Stone / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.035)
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.09),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.09),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
cube('Lid / brass inset surround',(0,0,1.989),(3.21,1.87,.024),gold,lid,.008)
cube('Lid / lagoon inset',(0,0,2.006),(3.13,1.79,.018),teal,lid,.006)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone / foot',(sx*1.47,sy*.91,-.095),(.54,.46,.32),stone,bevel=.06)
# Two low asymmetrical cupped valves, radial ridges modeled in their surfaces.
# Grid avoids collapsed poles and is solidified with a narrow rim.
def shell(name,upper=False):
 vs=[];fs=[];nu=48;nv=18
 for j in range(nv+1):
  t=j/nv
  for i in range(nu+1):
   a=-math.pi*.46+math.pi*.92*i/nu
   r=.13+.70*t;rib=math.sin(i/nu*math.pi*24)*.010*t
   x=math.sin(a)*r*(.73 if upper else .84)
   y=-.32+math.cos(a)*r*(.83 if upper else 1)
   z=2.085+.16*(t-.45)**2+rib
   if upper:
    # tilted rear valve opens away from the viewer; still low enough for lid clearance.
    y=.18+(.5-t)*.40;z=2.12+t*.51+rib;x*=.90
   vs.append((x,y,z))
 for j in range(nv):
  for i in range(nu):
   k=j*(nu+1)+i;fs.append((k,k+1,k+nu+2,k+nu+1))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(nacre)
 for f in me.polygons:f.use_smooth=True
 select(o);m=o.modifiers.new('Shell thickness','SOLIDIFY');m.thickness=.018;bpy.ops.object.modifier_apply(modifier=m.name);parent(o)
 return o
shell('Oyster / lower radial valve');shell('Oyster / raised radial valve',True)
cube('Shell mount / brass cradle',(0,.04,2.055),(.40,.42,.09),gold,lid,.02)
cube('Shell mount / nacre hinge',(0,.36,2.11),(.25,.15,.09),nacre,lid,.02)
bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=.19,location=(0,-.05,2.285));o=bpy.context.object;o.name='Pearl / central ivory';o.data.materials.append(pearl)
for f in o.data.polygons:f.use_smooth=True
parent(o)
# Fine inset decorative studs sit on the teal enamel rather than hidden in it.
for x in [-1.40,1.40]:
 for y in [-.72,.72]:
  bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.035,location=(x,y,2.034));o=bpy.context.object;o.name='Lid / brass stud';o.scale.z=.45;o.data.materials.append(gold);parent(o)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.27
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'bahrain.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'bahrain.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('AUTHOR PASS: Bahrain Pearl & Coral Stone')
