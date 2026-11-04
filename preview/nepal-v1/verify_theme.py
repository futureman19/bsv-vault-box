import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'nepal.blend'),use_scripts=False)
bpy.context.view_layer.update()
mountains=[o for o in bpy.data.objects if o.name.startswith('Mountain /')]
if '--negative' in sys.argv: mountains[0].parent=None
checks={};checks['three_peaks']=len(mountains)==3
checks['lid_ownership']=all(o.parent and o.parent.name=='Lid_Hinge' for o in mountains)
bounds=[]
for o in mountains:
 vs=[o.matrix_world@v.co for v in o.data.vertices];bounds.append([[min(v[i] for v in vs),max(v[i] for v in vs)] for i in range(3)])
checks['root_seating']=all(abs(b[2][0]-1.974)<1e-5 for b in bounds)
checks['height_contract']=all(abs(b[2][1]-z)<1e-5 for b,z in zip(bounds,[2.598,2.928,2.698]))
checks['separate_ornaments']=all(bounds[i][0][1]<bounds[i+1][0][0] for i in range(2))
checks['two_material_snow_slopes']=all(len(o.data.materials)==2 and set(f.material_index for f in o.data.polygons)=={0,1} for o in mountains)
checks['packed_maps']=sum(bool(i.packed_file) for i in bpy.data.images)>=3
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'bounds':bounds,'negative_control':'detached first mountain' if '--negative' in sys.argv else None}
(R/('theme-negative.json' if '--negative' in sys.argv else 'theme-check.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result));assert all(checks.values()),checks
