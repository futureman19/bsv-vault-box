"""Import exact portable candidate into original studio. Editable evaluated meshes.
Original procedural source is untouched. No Blender-only material recreation.
"""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'original/iceland.blend'),use_scripts=False)
for o in list(bpy.data.objects):
 if o.type in {'MESH','EMPTY'} and not o.name.startswith('Studio'):bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(R/'iceland.glb'))
for im in bpy.data.images:
 if im.has_data:im.pack()
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'iceland.blend'))
bpy.context.scene.render.resolution_x=1200;bpy.context.scene.render.resolution_y=960
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('EDITABLE_PORTABLE_MATERIALS_SAVED')
