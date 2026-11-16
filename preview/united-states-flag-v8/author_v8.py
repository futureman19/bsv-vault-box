"""V8 structural upper-shell refinement, mapped in physical developed units."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline-v7.blend'),use_scripts=False)
bpy.context.view_layer.update()
def zmap(z):return z if z<=1.56 else 1.56+(z-1.56)*.20
# Snapshot closed world vertices, then re-seat empties and all affected hardware.
objects=[o for o in bpy.data.objects if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']]
dep=bpy.context.evaluated_depsgraph_get()
for o in objects:
 if o.type=='MESH' and len(o.modifiers):
  evaluated=bpy.data.meshes.new_from_object(o.evaluated_get(dep));o.modifiers.clear();o.data=evaluated
bpy.context.view_layer.update()
world={o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in objects if o.type=='MESH'}
matrices={o.name:o.matrix_world.copy() for o in objects}
def depth(o):return 0 if o.parent is None else 1+depth(o.parent)
for o in sorted(objects,key=depth):
 m=matrices[o.name].copy();m.translation.z=zmap(m.translation.z);o.matrix_world=m;bpy.context.view_layer.update()
for o in objects:
 if o.type!='MESH':continue
 inv=o.matrix_world.inverted()
 for v,w in zip(o.data.vertices,world[o.name]):
  w.z=zmap(w.z)
  if o.name=='Flag / clasp seat':w.z=1.125+(w.z-1.125)*(1.53-1.125)/(1.567-1.125)
  if o.name.startswith('Hinge / bearing mounting stem'):w.y=1.26+(w.y-1.26)*.5
  if o.name=='Lid / polished slab':
   for axis,old,new in [(0,1.815,1.848),(1,1.145,1.178)]:
    a=abs(w[axis]);w[axis]=math.copysign(a*new/old if a<=old else new+(a-old)*.012/.045,w[axis])
  v.co=inv@w
 o.data.update()
for name in ['flag-lid.png','flag-wall.png']:
 im=bpy.data.images.get(name);im.unpack(method='REMOVE');im.filepath=str(R/'maps'/name);im.reload();im.pack()
bpy.context.view_layer.update()
r=.012
lengths=[math.hypot(r*(math.sin((i+1)*math.pi/6)-math.sin(i*math.pi/6)),(.009)*(math.cos((i+1)*math.pi/6)-math.cos(i*math.pi/6))) for i in range(3)]
arc=sum(lengths)
def piece(angle,ls):
 u=min(3,max(0,angle/(math.pi/6)));i=min(2,int(u));return sum(ls[:i])+ls[i]*(u-i)
def developed(out,z):
 if z>=1.6346-1e-6:return piece(math.atan2(max(0,out)/r,max(0,z-1.6346)/.009),lengths)
 if z>=1.5926:return arc+1.6346-z
 if z>=1.5836-1e-6:return arc+.042+piece(math.atan2(max(0,1.5926-z)/.009,max(0,out)/r),list(reversed(lengths)))
 return 2*arc+.042+1.5836-z
lid=bpy.data.objects['Lid / polished slab'];mat=lid.data.materials[0]
for o in objects:
 if o.type!='MESH':continue
 islid=o==lid
 if o.name.startswith('Flag body /'):
  uv=o.data.uv_layers.active
  for p in o.data.polygons:
   for li in p.loop_indices:
    co=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
    if abs(p.normal.y)>=abs(p.normal.x):s=8.06+co.x if co.y<0 else 1.86-co.x
    else:s=4.96-co.y if co.x<0 else 11.16+co.y
    uv.data[li].uv=(s/12.4,(co.z-.10)/1.46)
 isseam=o.name.startswith(('Navy seam /','Flag / rim corner'))
 if not (islid or isseam):continue
 if isseam:o.data.materials.clear();o.data.materials.append(mat)
 uv=o.data.uv_layers.active
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co;x,y=co.x,co.y
   if islid:
    if p.normal.z<-.999:x=math.copysign(1.848+2*arc+.042,x);y=math.copysign(1.178+2*arc+.042,y)
    else:
     if abs(x)>=1.848-1e-6 and abs(p.normal.x)>1e-5:x=math.copysign(1.848+developed(abs(x)-1.848,co.z),x)
     if abs(y)>=1.178-1e-6 and abs(p.normal.y)>1e-5:y=math.copysign(1.178+developed(abs(y)-1.178,co.z),y)
   else:
    q=2*arc+.042+1.5836-co.z
    if abs(p.normal.x)>.5:x=math.copysign(1.848+q,x)
    if abs(p.normal.y)>.5:y=math.copysign(1.178+q,y)
   uv.data[li].uv=((x+2.56)/5.12,(y+1.89)/3.78)
for m in bpy.data.materials:
 if not m.use_nodes:continue
 for n in m.node_tree.nodes:
  if n.type=='BSDF_PRINCIPLED':
   if 'Gold' in m.name or 'Brass' in m.name:n.inputs['Roughness'].default_value=.23
   elif 'Flag' in m.name or 'lacquer' in m.name.lower():
    n.inputs['Coat Weight'].default_value=.38;n.inputs['Coat Roughness'].default_value=.19
scene=bpy.context.scene;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.resolution_percentage=75;scene.cycles.samples=48
bpy.ops.wm.save_as_mainfile(filepath=str(R/'united-states.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=lid
bpy.ops.export_scene.gltf(filepath=str(R/'united-states.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'blender-source-no-fx.png');bpy.ops.render.render(write_still=True)
print('V8 geometry CHANGED: upper shell .30 to .06, affected hardware and pivot seating remapped; requires full verification')
