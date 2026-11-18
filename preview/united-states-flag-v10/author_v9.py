"""V10 seam-star refinement from substantial V7 baseline; one profile correction."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline-v7.blend'),use_scripts=False)
bpy.context.view_layer.update()
def linear(n):
 s=n/255
 return s/12.92 if s<=.04045 else ((s+.055)/1.055)**2.4
red=tuple(linear(x) for x in (181,0,24))+(1,)
navy=tuple(linear(x) for x in (2,31,65))+(1,)
changes=[]
for m in bpy.data.materials:
 if not m.use_nodes:continue
 for n in m.node_tree.nodes:
  if n.type!='BSDF_PRINCIPLED':continue
  inp=n.inputs['Base Color']
  if inp.is_linked:continue
  old=list(inp.default_value)
  # Explicit flag lacquer pigments; preserve gold, ivory, interior and dark bearings.
  if 'red' in m.name.lower() or 'navy' in m.name.lower():
   color=red if 'red' in m.name.lower() else navy
   inp.default_value=color;m.diffuse_color=color;changes.append(dict(material=m.name,before=old,after=list(color)))
for name in ['flag-lid.png','flag-wall.png','lacquer-roughness.png']:
 im=bpy.data.images.get(name)
 if im.packed_file:im.unpack(method='REMOVE')
 im.filepath=str(R/'maps'/name);im.reload();im.pack()
# Correction 1: align the fixed navy rim with the lid's vertical skirt.
# The 0.30 lid and hinge/latch pivots stay unchanged; only shallow rim profiles move.
for o in bpy.data.objects:
 if o.type!='MESH':continue
 if o.name.startswith('Navy seam / side'):
  for v in o.data.vertices:
   w=o.matrix_world@v.co
   if abs(w.x)>1.78:w.x=1.86 if w.x>0 else -1.86
   v.co=o.matrix_world.inverted()@w
 if o.name=='Navy seam / long':
  for v in o.data.vertices:
   w=o.matrix_world@v.co
   if w.y < -1.15:w.y=-1.19
   v.co=o.matrix_world.inverted()@w
 if o.name.startswith('Flag / rim corner'):
  for v in o.data.vertices:
   w=o.matrix_world@v.co
   if w.y < -1.15:w.y=-1.19
   v.co=o.matrix_world.inverted()@w
 if o.name=='Lid / polished slab' or o.name.startswith(('Navy seam /','Flag / rim corner')):
  for mod in o.modifiers:
   if mod.type=='BEVEL':mod.width=.008
bpy.context.view_layer.update()
# Re-register existing pigment UVs in closed world space.
import math
arc=3*2*.045*math.sin(math.pi/12)
for o in bpy.data.objects:
 if o.type!='MESH' or not o.data.uv_layers.active:continue
 mats=[m.name for m in o.data.materials]
 if 'Flag / lacquer' in mats:
  for p in o.data.polygons:
   for li in p.loop_indices:
    v=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
    o.data.uv_layers.active.data[li].uv.y=(v.z-.10)/(1.978-.10)
 if o.name=='Lid / polished slab':
  for p in o.data.polygons:
   n=o.matrix_world.to_3x3()@p.normal
   if max(abs(n.x),abs(n.y))<.1:continue
   for li in p.loop_indices:
    v=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
    q=arc+1.933-v.z
    if abs(n.x)>abs(n.y):x=(-1.815-q) if n.x<0 else (1.815+q);y=v.y
    else:x=v.x;y=(-1.145-q) if n.y<0 else (1.145+q)
    o.data.uv_layers.active.data[li].uv=((x+2.56)/5.12,(y+1.89)/3.78)
scene=bpy.context.scene;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_percentage=75;scene.cycles.samples=48
lid=bpy.data.objects['Lid / polished slab'];coords=[lid.matrix_world@v.co for v in lid.data.vertices]
report=dict(lid_min_z=min(v.z for v in coords),lid_max_z=max(v.z for v in coords),lid_thickness=max(v.z for v in coords)-min(v.z for v in coords),pigments=changes,pivots={n:list(bpy.data.objects[n].matrix_world.translation) for n in ['Lid_Hinge','Latch_Pivot']},restoration='V7 substantial lid and pivots; V10 rim profile/bevel and UV correction')
(R/'author-check.json').write_text(json.dumps(report,indent=2));print(report)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'united-states.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid
bpy.ops.export_scene.gltf(filepath=str(R/'united-states.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'blender-source-no-fx.png');bpy.ops.render.render(write_still=True)
