import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
def snap(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update()
 return {o.name:{'matrix':list(sum((list(row) for row in o.matrix_world),[])),'parent':o.parent.name if o.parent else None,'vertices':[list(v.co) for v in o.data.vertices] if o.type=='MESH' else None,'faces':[list(p.vertices) for p in o.data.polygons] if o.type=='MESH' else None} for o in bpy.data.objects}
a=snap(R/'original/iceland.blend');b=snap(R/'iceland.blend');assert a==b
images=[i for i in bpy.data.images if i.name.startswith('basalt-')];assert len(images)==3 and all(i.packed_file and list(i.size)==[256,256] for i in images)
assert all(o.data.uv_layers.get('BasaltUV') for o in bpy.data.objects if o.name.startswith('Basalt column'))
r={'independent_reopen':True,'all_object_matrices_parents_vertices_faces_identical':True,'packed_256_images':[i.name for i in images],'basalt_uv_present':True};(R/'editable-check.json').write_text(json.dumps(r,indent=2));print(r)
