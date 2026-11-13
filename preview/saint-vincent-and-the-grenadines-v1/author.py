"""Soufrière & Cays: original procedural landscape miniature, not a scale map."""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(3317921)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def uv(o,axis='X'):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone physical projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(p.normal[i]));axes=[i for i in range(3) if i!=axis]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.7,co[axes[1]]*.7)
exec((R/'geometry_helpers.py').read_text())
stone=mat('Volcanic stone / fine porous charcoal',(.034,.047,.045),.78)
maptex(stone,'volcanic-color.png','Base Color');maptex(stone,'volcanic-roughness.png','Roughness',True)
t=stone.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/volcanic-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();normal=stone.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.35;stone.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);stone.node_tree.links.new(normal.outputs['Normal'],stone.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
sea=mat('Sea / turquoise enamel',(.021,.26,.30),.24,.12)
sand=mat('Sand / pale cay margins',(.67,.58,.36),.83)
green=mat('Forest / deep green',(.035,.105,.048),.89)
ash=mat('Crater / ash charcoal',(.065,.07,.063),.93)
seam=mat('Seam / dark mineral green',(.023,.045,.031),.92)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Body / volcanic long',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.027)
for sx in [-1,1]:cube('Body / volcanic end',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.027)
cube('Body / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.14 if sy<0 else .07,.09),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / end',(sx*1.74,0,1.618),(.16,2.05,.09),seam,bevel=.009)
 for sy in [-1,1]:cube('Body / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
cube('Sea / inset',(0,0,1.982),(3.26,1.94,.018),sea,lid,.006)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Foot / volcanic',(sx*1.47,sy*.91,-.07),(.53,.45,.35),stone,bevel=.055)
def mesh(n,vs,fs,materials,indices=None):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o)
 for m in materials:me.materials.append(m)
 if indices:
  for p,i in zip(me.polygons,indices):p.material_index=i
 uv(o);parent(o);return o
# Five asymmetrical sand-edged cays: ring mesh with distinct green centre relief.
cays=[(.18,-.60,.21,.13),(.76,-.54,.20,.14),(1.20,-.13,.18,.15),(.74,.16,.22,.16),(1.12,.61,.20,.13)]
for k,(cx,cy,rx,ry) in enumerate(cays):
 n=24;vs=[]
 for ring in range(3):
  for j in range(n):
   a=j*math.tau/n;ir=1+.09*math.sin(3*a+k)+.06*math.cos(5*a+k);scale=[1,.75,.40][ring];z=[1.987,2.024,2.065][ring]
   vs.append((cx+rx*ir*scale*math.cos(a),cy+ry*ir*scale*math.sin(a),z+.009*math.sin(a*4+k)*(ring>0)))
 vs.append((cx,cy,2.075));fs=[];inds=[]
 for ring in range(2):
  for j in range(n):fs.append((ring*n+j,ring*n+(j+1)%n,(ring+1)*n+(j+1)%n,(ring+1)*n+j));inds.append(ring)
 for j in range(n):fs.append((2*n+j,2*n+(j+1)%n,3*n));inds.append(1)
 mesh('Cay / '+str(k+1),vs,fs,[sand,green],inds)
# Explicit crater rings: uneven outer flanks, high broken rim, recessed bowl.
n=64;cx=-.65;cy=.30;vs=[]
for ring in range(5):
 for j in range(n):
  a=j*math.tau/n;rad=[1,.72,.38,.25,.10][ring];jitter=1+.09*math.sin(3*a)+.04*math.cos(7*a)
  z=[1.987,2.15,2.49,2.43,2.23][ring]+[0,.055,.055,.035,.01][ring]*math.sin(3*a+.3)
  vs.append((cx+.60*rad*jitter*math.cos(a),cy+.47*rad*jitter*math.sin(a),z))
vs.append((cx,cy,2.225));fs=[];inds=[]
for ring in range(4):
 for j in range(n):fs.append((ring*n+j,ring*n+(j+1)%n,(ring+1)*n+(j+1)%n,(ring+1)*n+j));inds.append(0 if ring<2 else 1)
for j in range(n):fs.append((4*n+j,4*n+(j+1)%n,5*n));inds.append(1)
mesh('Soufriere / crater massif',vs,fs,[green,ash],inds)
# Sparse low reef arc in the water, intentionally schematic (not coral specimens).
vs=[];fs=[]
for j in range(41):
 a=-1.6+j/40*3.0
 for r in [0,1]:vs.append((.70+(1.00+r*.022)*math.cos(a),-.02+(.85+r*.018)*math.sin(a),1.994))
for j in range(40):fs.append((2*j,2*j+1,2*j+3,2*j+2))
mesh('Reef / horseshoe trace',vs,fs,[sand])
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.26
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.0));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.8
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=900;scene.render.resolution_y=720;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'saint-vincent-and-the-grenadines.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'saint-vincent-and-the-grenadines.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('AUTHOR PASS')
