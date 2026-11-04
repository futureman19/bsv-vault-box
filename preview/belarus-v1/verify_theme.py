import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'belarus.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in pivots.items():assert max(abs(v-bpy.data.objects[n].matrix_world[i][j]) for i,row in enumerate(rows) for j,v in enumerate(row))<1e-6
warp=[o for o in bpy.data.objects if o.name.startswith('Weave / warp')];weft=[o for o in bpy.data.objects if o.name.startswith('Weave / weft')]
assert len(warp)==21 and len(weft)==13
if '--negative' in sys.argv:warp[0].parent=None
assert all(o.parent==bpy.data.objects['Lid_Hinge'] for o in warp+weft),'Detached ribbon rejected'
verts=[o.matrix_world@v.co for o in warp+weft for v in o.data.vertices]
lo=min(v.z for v in verts);hi=max(v.z for v in verts)
assert 1.978<=lo<=2.0 and hi<2.09,(lo,hi)
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
# Probe top of backing through an inter-ribbon opening.
hit,loc,normal,idx,obj,mat=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((.06,.06,2.2)),Vector((0,0,-1)))
assert hit and obj.name=='Weave / backing',(obj.name,loc[:])
result=dict(status='PASS',warp=21,weft=13,lid_parentage=True,height=[lo,hi],backing_gap_ray=loc.z,pivots_preserved=True,slab_dimensions=list(slab.dimensions))
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
