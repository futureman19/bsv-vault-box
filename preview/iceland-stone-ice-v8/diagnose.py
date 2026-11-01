import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(R/'iceland.glb'))
errors=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();bad=[]
 for t in m.loop_triangles:
  a,b,c=[m.vertices[i].co for i in t.vertices]
  if (b-a).cross(c-a).length_squared<1e-18:bad.append(t.index)
 if bad:errors.append([o.name,len(bad)])
print(errors);(R/'degenerate-diagnosis.json').write_text(json.dumps(errors,indent=2))
