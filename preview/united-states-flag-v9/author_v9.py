"""Restore exact V7 substantial source geometry and seating; change only requested pigments."""
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
scene=bpy.context.scene;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_percentage=75;scene.cycles.samples=48
lid=bpy.data.objects['Lid / polished slab'];coords=[lid.matrix_world@v.co for v in lid.data.vertices]
report=dict(lid_min_z=min(v.z for v in coords),lid_max_z=max(v.z for v in coords),lid_thickness=max(v.z for v in coords)-min(v.z for v in coords),pigments=changes,pivots={n:list(bpy.data.objects[n].matrix_world.translation) for n in ['Lid_Hinge','Latch_Pivot']},restoration='Exact packed V7 geometry, UVs, hardware and pivots; not a reverse deformation of V8')
(R/'author-check.json').write_text(json.dumps(report,indent=2));print(report)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'united-states.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid
bpy.ops.export_scene.gltf(filepath=str(R/'united-states.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'blender-source-no-fx.png');bpy.ops.render.render(write_still=True)
