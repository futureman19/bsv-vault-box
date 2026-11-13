import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'uganda.blend'),use_scripts=False)
bpy.context.view_layer.update()
o=bpy.data.objects['Mutuba / folded barkcloth']
if '--negative' in sys.argv:o.parent=None
checks={}
checks['lid_ownership']=o.parent is not None and o.parent.name=='Lid_Hinge'
v=[o.matrix_world@v.co for v in o.data.vertices];top=v[:53*29]
checks['xy_bounds']=all(abs(p.x)<=1.30001 and abs(p.y)<=.72001 for p in v)
checks['top_bounds']=min(p.z for p in top)>=2.04 and max(p.z for p in top)<=2.18
checks['skirt_seated']=abs(min(p.z for p in v)-1.978)<1e-5
checks['upward_top']=all(f.normal.z>0 for f in list(o.data.polygons)[:52*28])
checks['hollow_body']=bpy.data.objects.get('Interior floor') is not None
checks['three_maps_packed']=len([i for i in bpy.data.images if i.packed_file])>=3
r={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'top_min':min(p.z for p in top),'top_max':max(p.z for p in top),'note':'Negative control deliberately removes lid ownership; not a model defect.' if '--negative' in sys.argv else 'Saved-source measured contract'}
(R/('negative-control.json' if '--negative' in sys.argv else 'theme-check.json')).write_text(json.dumps(r,indent=2));print(json.dumps(r));assert all(checks.values())
