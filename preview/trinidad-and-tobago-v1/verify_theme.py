import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'trinidad-and-tobago.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
pans=[o for o in bpy.data.objects if o.name.startswith('Pan /')]
notes=[o for o in pans if 'note ' in o.name];bowls=[o for o in pans if 'bowl ' in o.name]
def owned(objects):return all(o.parent==lid for o in objects)
assert len(notes)==22 and len(bowls)==2 and len(pans)==28 and owned(pans)
notes[0].parent=None
assert not owned(pans),'detached negative control must fail'
notes[0].parent=lid
bad=[o.name for o in notes+bowls if any(p.normal.z<=0 for p in o.data.polygons)]
report={'pan_meshes':len(pans),'notes':len(notes),'bowls':len(bowls),'all_lid_owned':True,'detached_negative_rejected':True,'downward_surface_normals':bad}
(R/'theme-check.json').write_text(json.dumps(report,indent=2))
assert not bad,('downward playing-surface normals',bad)
for o in bowls:
 v=[o.matrix_world@v.co for v in o.data.vertices]
 assert abs(min(p.z for p in v)-2.04)<1e-5 and abs(max(p.z for p in v)-2.24)<1e-5
 assert max(p.x for p in v)-min(p.x for p in v)>1.25
report['concavity_depth']=.20
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for n,m in pivots.items() for i in range(4) for j in range(4))
assert err<1e-7
report['baseline_pivot_max_error']=err;report['status']='PASS'
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print('THEME PASS',json.dumps(report))
