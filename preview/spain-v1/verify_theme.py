import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
# Independently evaluate both files, never compare unevaluated appended objects.
def pivots(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update()
 return {n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
baseline=pivots(R/'mechanism.blend');actual=pivots(R/'spain.blend');assert baseline==actual
lid=bpy.data.objects['Lid_Hinge']
def check():
 petals=[o for o in bpy.data.objects if o.name.startswith('Lid ornament / cobalt petal')]
 ornaments=[o for o in bpy.data.objects if o.name.startswith('Lid ornament')]
 assert len(petals)==8
 assert len([o for o in ornaments if 'border' in o.name])==32
 assert len([o for o in ornaments if 'ochre bead' in o.name])==8
 assert all(o.parent==lid for o in ornaments),'detached lid ornament'
 assert max((o.matrix_world@v.co).z for o in ornaments for v in o.data.vertices)<2.20
 slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
 assert len([o for o in bpy.data.objects if o.name.startswith('Glaze panel')])==4
 return {'petals':len(petals),'ornaments':len(ornaments),'borders':32,'beads':8,'lid_dimensions':list(slab.dimensions)}
r=check();o=bpy.data.objects['Lid ornament / cobalt petal'];o.parent=None
try:check()
except AssertionError as e:negative=str(e)
else:raise AssertionError('negative control was accepted')
o.parent=lid;check()
r.update(status='PASS',pivot_matrices_equal=True,negative_detached_ornament_rejected=negative,brief_written_before_author=True)
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
