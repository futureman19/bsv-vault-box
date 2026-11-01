"""Run in Blender; authored before new geometry. Saved-source feature contracts."""
import bpy, math, json
from pathlib import Path
R=Path(__file__).resolve().parent
assert (R/'iceland.blend').exists(), 'RED: new authored source missing'
bpy.ops.wm.open_mainfile(filepath=str(R/'iceland.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge']
def meshes(prefix): return [o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(prefix)]
river=meshes('River /'); glacier=meshes('Glacier /'); rocks=meshes('Basalt fracture'); caps=meshes('Corner strap'); moss=meshes('Sheltered moss')
assert river and glacier and len(rocks)>40 and len(caps)>=24 and len(moss)>30
assert all(o.parent==lid and len(o.data.polygons)>0 for o in river+glacier)
bpy.context.view_layer.update()
peak=max((o.matrix_world@v.co).z for o in glacier for v in o.data.vertices)
assert 2.05<peak<2.5, peak
assert len({round(o['recess'],3) for o in rocks})>12
assert len(meshes('Strap rivet'))>=32
mat=bpy.data.materials['Polished black obsidian'];p=mat.node_tree.nodes.get('Principled BSDF')
assert max(p.inputs['Base Color'].default_value[:3])<.009 and p.inputs['Roughness'].default_value<.2
bad=[];triangles=0
for o in [o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')]:
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles()
 for t in m.loop_triangles:
  a,b,c=[m.vertices[i].co for i in t.vertices];triangles+=1
  if not all(math.isfinite(x) for v in (a,b,c) for x in v) or (b-a).cross(c-a).length_squared<1e-18:bad.append(o.name)
 ev.to_mesh_clear()
assert not bad,bad
result=dict(river_meshes=len(river),glacier_meshes=len(glacier),glacier_peak=peak,fracture_blocks=len(rocks),corner_strap_parts=len(caps),moss_patches=len(moss),triangles=triangles,degenerate=bad)
(R/'features-check.json').write_text(json.dumps(result,indent=2));print(result)
