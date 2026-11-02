"""Bangladesh: original Jamdani-inspired inlay and tidal delta miniature.
Blender-script authored; read-only trimmed family mechanism is included.
"""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(879)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.preferences.filepaths.save_version=0
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'helpers.py').read_text())
cloth=mat('Jamdani / original ivory repeats',(.02,.08,.08),.58)
maptex(cloth,'jamdani-color.png','Base Color');maptex(cloth,'weave-roughness.png','Roughness',True)
t=cloth.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/weave-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();normal=cloth.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.22;cloth.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);cloth.node_tree.links.new(normal.outputs['Normal'],cloth.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
frame=mat('Lacquer / deep tidal teal',(.012,.055,.052),.31)
liner=mat('Interior / warm dark textile',(.07,.095,.08),.8)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
ivory=mat('Ivory / woven border',(.66,.55,.35),.5)
seam=mat('Seam / deep teal',(.01,.025,.02),.9)
water=mat('Delta / blue green enamel water',(.022,.20,.22),.19,.15)
land=mat('Delta / green alluvial islands',(.035,.12,.05),.84);maptex(land,'delta-green.png','Base Color')
silt=mat('Delta / silt banks',(.24,.21,.09),.85)
leaf=mat('Delta / mangrove canopy',(.025,.085,.028),.9)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
# Solid outer skins overlay the unchanged hollow inner shell.
for sy in [-1,1]:
 o=cube('Jamdani / '+('front' if sy<0 else 'rear'),(0,sy*1.145,.83),(3.72,.19,1.46),cloth,bevel=.018)
for sx in [-1,1]:
 o=cube('Jamdani / side',(sx*1.765,0,.83),(.19,2.1,1.46),cloth,bevel=.018,axis='Y')
# Correct aspect-aware textile UV: original helper's X/Y projection is scaled for each face.
for o in bpy.data.objects:
 if o.name.startswith('Jamdani'):
  for p in o.data.polygons:
   for li in p.loop_indices:
    v=o.data.vertices[o.data.loops[li].vertex_index].co
    u=v.y if 'side' in o.name else v.x
    o.data.uv_layers.active.data[li].uv=(u/3.72+.5,v.z/3.72+.5)
for z in [.15,1.49]:
 for sy in [-1,1]:cube('Frame / horizontal welt',(0,sy*1.246,z),(3.72,.035,.045),gold,bevel=.01)
 for sx in [-1,1]:cube('Frame / side welt',(sx*1.871,0,z),(.035,2.42,.045),gold,bevel=.01)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Frame / corner upright',(sx*1.79,sy*1.20,.82),(.15,.13,1.42),frame,bevel=.025)
  cube('Foot / brass shoe',(sx*1.49,sy*.91,-.08),(.40,.35,.33),gold,bevel=.07)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),frame,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),frame,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),frame,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# The water is one connected low-relief inset; islands split it into branching tidal channels.
cube('Delta / connected tidal water',(0,0,1.999),(3.19,1.85,.038),water,lid,.025)
for sy in [-1,1]:cube('Lid border / long',(0,sy*.96,2.005),(3.30,.045,.035),gold,lid,.009)
for sx in [-1,1]:cube('Lid border / side',(sx*1.64,0,2.005),(.045,1.96,.035),gold,lid,.009)
# Repeated stepped ivory border marks, geometry rather than painted lid edging.
for sy in [-1,1]:
 for i in range(19):
  o=cube('Lid ornament / ivory lozenge',(-1.48+i*.164,sy*1.055,1.994),(.045,.045,.015),ivory,lid,.003);o.rotation_euler.z=math.pi/4
# Four disjoint irregular island polygons surround visible connected branches.
polygons=[
 [(-1.50,-.82),(-.38,-.82),(-.28,-.62),(-.38,-.43),(-.32,-.28),(-.60,-.08),(-.94,-.15),(-1.22,-.06),(-1.50,-.16)],
 [(-1.50,.08),(-1.20,.18),(-.91,.08),(-.61,.15),(-.37,.35),(-.31,.58),(-.15,.82),(-1.50,.82)],
 [(-.14,-.82),(1.50,-.82),(1.50,-.15),(1.21,-.24),(.98,-.13),(.73,-.30),(.51,-.23),(.19,-.41),(-.07,-.47)],
 [(.09,-.23),(.45,-.02),(.72,-.08),(.99,.10),(1.25,-.01),(1.50,.10),(1.50,.82),(.09,.82),(-.10,.55),(-.14,.30)] ]
def island(n,poly):
 # Subdivide banks with small irregular undulations: narrow channels stay open.
 refined=[]
 for i,a in enumerate(poly):
  b=poly[(i+1)%len(poly)];dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
  for k in range(6):
   t=k/6;off=math.sin(t*math.pi)*random.uniform(-.025,.025)
   refined.append((a[0]+dx*t-dy/length*off,a[1]+dy*t+dx/length*off))
 poly=refined;z0=2.013;z1=2.065
 N=len(poly);cx=sum(p[0] for p in poly)/N;cy=sum(p[1] for p in poly)/N
 verts=[(x,y,z0) for x,y in poly]+[(cx+(x-cx)*.98,cy+(y-cy)*.98,z1+random.uniform(-.004,.004)) for x,y in poly]+[(cx,cy,2.105)]
 faces=[]
 for i in range(N):
  j=(i+1)%N;faces.append((i,j,N+j,N+i));faces.append((N+i,N+j,2*N))
 faces.append(tuple(reversed(range(N))))
 mesh=bpy.data.meshes.new(n);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(n,mesh);bpy.context.collection.objects.link(o);mesh.materials.append(land);mesh.materials.append(silt)
 for i,f in enumerate(mesh.polygons):f.material_index=1 if i%2==0 and i<2*N else 0
 uv(o);parent(o);return cx,cy
for i,poly in enumerate(polygons):
 cx,cy=island('Delta / island '+str(i+1),poly)
 # Small angular clustered canopy relief, not a tall tree or realistic species model.
 for j in range(5):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(cx+(j-2)*.065,cy+random.uniform(-.08,.08),2.11))
  o=bpy.context.object;o.name='Delta / canopy '+str(i+1);o.scale=(.11,.085,.055);o.data.materials.append(leaf);parent(o)
# Remove obsolete inherited unused resources; studio remains source-only.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.26
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.7));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.05))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.65
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'bangladesh.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'bangladesh.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('BANGLADESH AUTHORED')
