import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'timor-leste.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];runner=bpy.data.objects['Runner / waved textile']
if '--negative-control' in sys.argv:runner.parent=None
checks={}
checks['runner_lid_parent']=runner.parent==lid
vs=[runner.matrix_world@v.co for v in runner.data.vertices]
zs=[v.z for v in vs[:49*25]]
checks['runner_top_height']=min(zs)>=2.008 and max(zs)<=2.052
checks['runner_xy_contract']=abs(min(v.x for v in vs)+1.55)<1e-5 and abs(max(v.x for v in vs)-1.55)<1e-5 and abs(max(v.y for v in vs)-.82)<1e-5
fr=[o for o in bpy.data.objects if o.name.startswith('Fringe /')]
checks['56_lid_fringe_strands']=len(fr)==56 and all(o.parent==lid for o in fr)
checks['four_body_cloth_panels']=len([o for o in bpy.data.objects if o.name.startswith('Cloth /')])==4
checks['original_pivots']=tuple(round(v,4) for v in lid.location)==(0,1.32,1.668)
checks['packed_maps']=len([i for i in bpy.data.images if i.packed_file])>=3
report={'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL','runner_top_min':min(zs),'runner_top_max':max(zs),'fringe_count':len(fr),'negative_control':'detached runner' if '--negative-control' in sys.argv else None}
(R/('theme-negative-control.json' if '--negative-control' in sys.argv else 'theme-check.json')).write_text(json.dumps(report,indent=2));print(json.dumps(report));assert all(checks.values()),report
