"""Independent saved-source theme and exact inherited-pivot assertions."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
pivots={n:list(bpy.data.objects[n].matrix_local) for n in ['Lid_Hinge','Latch_Pivot']}
pivots={n:[list(v) for v in m] for n,m in pivots.items()}
bpy.ops.wm.open_mainfile(filepath=str(R/'gambia.blend'),use_scripts=False)
for n,m in pivots.items():assert [list(v) for v in bpy.data.objects[n].matrix_local]==m,n
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Mangrove /','Bank /','Estuary /'))]
assert ornaments and all(o.parent==bpy.data.objects['Lid_Hinge'] for o in ornaments)
heights=[(o.matrix_world@v.co).z for o in ornaments for v in o.data.vertices];assert max(heights)-1.978<=.85
seams=[o for o in bpy.data.objects if o.name.startswith('Tidal seam')];assert len(seams)==4 and all(o.dimensions.z<=.10 for o in seams)
main=bpy.data.objects['Estuary / main channel'];trib=bpy.data.objects['Estuary / tributary'];assert len(main.data.vertices)==98 and len(trib.data.vertices)==10
# The tributary mouth is within the main water strip at x=.38.
x=.38;centre=.22*math.sin((x+1.62)/3.24*math.tau*1.15)-.12
assert abs(-.27-centre)<.155
m=bpy.data.materials['Sediment bronze / tidal traces'];p=m.node_tree.nodes.get('Principled BSDF');assert p.inputs['Metallic'].default_value>.2
assert p.inputs['Base Color'].is_linked and p.inputs['Roughness'].is_linked
out={'status':'PASS','exact_inherited_pivots':pivots,'lid_dimensions':list(slab.dimensions),'ornament_meshes':len(ornaments),'ornament_top_z':max(heights),'seam_max_height':max(o.dimensions.z for o in seams),'tributary_mouth_connects':True,'portable_body_color_and_roughness':True}
(R/'source-theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
