"""Authored procedural geometry, not exact image reconstruction. Regeneration overwrites outputs."""
import bpy, math, random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
random.seed(73)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials): bpy.data.materials.remove(d)
def material(name,c,metal=0,rough=.5,emission=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*c,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emission
 return m
stones=[material('Basalt / facet %02d'%i,(.016+i*.003,.021+i*.003,.026+i*.003),.04,.78) for i in range(5)]
obsidian=material('Polished blue-black lid',(.018,.028,.036),.28,.29)
inside=material('Dark stone interior',(.018,.024,.029),.1,.65)
brass=material('Aged satin brass',(.39,.25,.095),.78,.31)
blue=material('Glacier mineral',(.10,.48,.64),.25,.28,.65)
parts=[]
def finish(o,name,mat,parent=None):
 o.name=name;o.data.materials.append(mat);parts.append(o)
 if parent:
  matrix=o.matrix_world.copy();o.parent=parent;o.matrix_world=matrix
 return o
def cube(name,loc,scale,mat,bevel=.03,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Soft worked edges','BEVEL');mod.width=min(bevel,min(scale)*.35);mod.segments=3
  o.modifiers.new('Weighted face normals','WEIGHTED_NORMAL')
 return finish(o,name,mat,parent)
def cyl(name,loc,r,depth,mat,rotation=(0,0,0),parent=None,vertices=24):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc,rotation=rotation)
 o=finish(bpy.context.object,name,mat,parent);mod=o.modifiers.new('Turned edge','BEVEL');mod.width=min(.012,depth*.2);mod.segments=2;o.modifiers.new('Normals','WEIGHTED_NORMAL');return o
def line(name,points,r,mat,parent=None):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=1
 s=c.splines.new('POLY');s.points.add(len(points)-1)
 for p,co in zip(s.points,points):p.co=(*co,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o)
 # Mesh conversion makes exported mineral geometry explicit.
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object;o.select_set(False)
 return finish(o,name,mat,parent)
def empty(name,loc,parent=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=loc
 if parent:
  bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=parent;o.matrix_world=mw
 return o
# Fully hollow, continuous structural liner; exposed faceted cladding outside.
cube('Interior floor',(0,0,.15),(3.42,2.12,.23),inside)
for y in [-.99,.99]:cube('Interior wall / front' if y<0 else 'Interior wall / rear',(0,y,.8),(3.42,.16,1.24),inside,.025)
for x in [-1.62,1.62]:cube('Interior wall / end',(x,0,.8),(.16,1.9,1.24),inside,.025)
# Irregular vertical polygon columns, angular cross-sections and staggered strata.
def column(name,x,y,rx,ry):
 n=6;verts=[]
 ring=[(math.cos(math.tau*j/n)*rx*(1+random.uniform(-.10,.10)),math.sin(math.tau*j/n)*ry*(1+random.uniform(-.1,.1))) for j in range(n)]
 levels=[.06,.51+random.uniform(-.14,.14),1.02+random.uniform(-.12,.12),1.405]
 for k,z in enumerate(levels):
  for a,b in ring:verts.append((x+a*(1 if k in [0,3] else random.uniform(.87,1.08)),y+b,z))
 faces=[tuple(reversed(range(n))),tuple(range(3*n,4*n))]
 for k in range(3):
  for j in range(n):faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
 for m in stones:mesh.materials.append(m)
 for f in mesh.polygons:f.material_index=random.randrange(len(stones))
 parts.append(o)
for y in [-1.07,1.07]:
 for i in range(12):column('Basalt column / long %s %02d'%(y,i),-1.61+i*.293,y,.177,.177)
for x in [-1.65,1.65]:
 for i in range(6):column('Basalt column / end %s %02d'%(x,i),x,-.77+i*.31,.17,.19)
# Fixed lip is below the lid swept volume.
for y in [-1.08,1.08]:cube('Glacial seam / rim',(0,y,1.435),(3.48,.028,.018),blue,.004)
for x in [-1.73,1.73]:cube('Glacial seam / end',(x,0,1.435),(.028,2.16,.018),blue,.004)
lid=empty('Lid_Hinge',(0,1.32,1.5));lid['mechanism']='negative local X, 0 to -105 degrees; latch releases first'
cube('Lid / polished slab',(0,0,1.66),(3.72,2.38,.30),obsidian,.09,lid)
cube('Lid / recessed inner face',(0,0,1.509),(3.31,1.98,.018),inside,.005,lid)
# Sparse irregular blue mineral, not a broad neon panel.
line('Lid / glacial fault',[(-1.81,.2,1.72),(-1.65,.18,1.812),(-1.15,.24,1.812),(-.82,.10,1.812),(-.32,.16,1.812),(.12,.06,1.812),(.43,.16,1.812),(.78,.11,1.812)],.009,blue,lid)
line('Lid / fault branch',[(-.82,.1,1.812),(-.71,.44,1.812),(-.5,.65,1.812)],.005,blue,lid)
for x in [-1.66,1.66]:
 for y in [-1.0,1.0]:
  cube('Lid / brass corner',(x,y,1.814),(.32,.31,.045),brass,.014,lid)
  cyl('Lid / corner rivet',(x,y,1.844),.035,.022,brass,parent=lid)
  cube('Foot / brass shoe',(x,y,.10),(.26,.26,.16),brass,.04)
for x in [-1.13,1.13]:
 # Barrels coaxial with exact hinge pivot; mounting ears are wholly behind body.
 cyl('Hinge / fixed barrel',(x,1.32,1.50),.075,.42,brass,(0,math.pi/2,0))
 cube('Hinge / fixed mount',(x,1.265,1.23),(.29,.06,.35),brass,.02)
 cube('Hinge / moving leaf',(x,1.25,1.59),(.28,.18,.18),brass,.015,lid)
cube('Latch / keeper',(0,-1.30,1.12),(.35,.09,.20),brass,.025)
latch=empty('Latch_Pivot',(0,-1.29,1.72),lid)
cyl('Latch / rotating knuckle',(0,-1.29,1.72),.073,.23,brass,(0,math.pi/2,0),latch)
cube('Latch / hinge bridge',(0,-1.36,1.70),(.24,.14,.06),brass,.012,latch)
cube('Latch / lifting hasp',(0,-1.425,1.40),(.24,.065,.60),brass,.022,latch)
cube('Latch / raised face',(0,-1.47,1.31),(.16,.035,.19),brass,.012,latch)
cyl('Latch / pin',(0,-1.30,1.72),.058,.34,brass,(0,math.pi/2,0),lid)
cyl('Medallion / decorative round',(0,-1.285,.69),.135,.048,brass,(math.pi/2,0,0))
cyl('Medallion / inset',(0,-1.313,.69),.095,.012,obsidian,(math.pi/2,0,0))
# Small abstract geological notch, no authenticity seal iconography.
line('Medallion / mountain',[(-.06,-1.325,.66),(0,-1.325,.73),(.06,-1.325,.66)],.008,brass)
# Lighting and camera are source-only, not part of collectible export.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True
scene.world.color=(.20,.20,.20)
def area(name,loc,power,color,size):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.color=color;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,.8))-o.location).to_track_quat('-Z','Y').to_euler()
area('Studio / key',(-3,-4,6),1000,(.80,.91,1),5)
area('Studio / gold rim',(4,2,4),1100,(1,.77,.46),4)
area('Studio / front',(1,-5,2.8),500,(.65,.80,1),3)
bpy.ops.object.camera_add(location=(5,-7,4.7));cam=bpy.context.object;cam.name='Poster camera';cam.rotation_euler=(Vector((0,0,.9))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.65;scene.camera=cam
scene.render.resolution_x=1500;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=True
scene.view_settings.view_transform='AgX'
# Studio floor deliberately excluded from GLB, and collision contract.
floor=cube('Studio / shadow floor',(0,0,-.045),(200,200,.04),material('Studio charcoal',(.018,.023,.029)),0);parts.remove(floor)
# Save independent editable source before exporting.
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'iceland.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[lid,latch]:o.select_set(True)
bpy.context.view_layer.objects.active=lid
bpy.ops.export_scene.gltf(filepath=str(ROOT/'iceland.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(ROOT/'poster.png');bpy.ops.render.render(write_still=True)
print('ICELAND_EXPORT_COMPLETE',len(parts))
