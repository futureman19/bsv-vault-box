import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
def pivots():
 bpy.context.view_layer.update();return {n:[v for row in bpy.data.objects[n].matrix_world for v in row] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);base=pivots()
bpy.ops.wm.open_mainfile(filepath=str(R/'poland.blend'),use_scripts=False);actual=pivots();assert base==actual
lid=bpy.data.objects['Lid_Hinge'];petals=[o for o in bpy.data.objects if o.name.startswith('Rosette / petal')];assert len(petals)==8
assert all(o.parent==lid for o in petals)
pts=[o.matrix_world@Vector(c) for o in petals for c in o.bound_box];zmax=max(p.z for p in pts);assert zmax-1.9985<=.20
front=bpy.data.objects['Ceramic / front'];assert abs(front.dimensions.x-3.72)<1e-5
seams=[o for o in bpy.data.objects if o.name.startswith('Cobalt seam')];assert len(seams)==4 and all(o.dimensions.z<=.08 for o in seams)
# Four repeated centerlines visible on the front UV-height interval.
uv=front.data.uv_layers.active;vs=[uv.data[i].uv.y for f in front.data.polygons if f.normal.y<-.9 for i in f.loop_indices];lo,hi=min(vs),max(vs)
rows=sum(lo<y/512<hi for y in range(-32,560,96));assert rows>=3
out={'status':'PASS','pivot_matrices_identical':base==actual,'petals':len(petals),'rosette_max_z':zmax,'front_width':front.dimensions.x,'front_motif_rows':rows,'seam_max_height':max(o.dimensions.z for o in seams)}
(R/'design-check.json').write_text(json.dumps(out,indent=2));print(out)
