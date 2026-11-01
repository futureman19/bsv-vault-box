import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
src=R/('approved-v7.blend' if '--baseline' in sys.argv else 'iceland.blend')
bpy.ops.wm.open_mainfile(filepath=str(src),use_scripts=False)
rocks=[o for o in bpy.data.objects if o.name.startswith('Basalt fracture')]
checks={}
checks['notched_all_four_sides']=all(any(side in o.name and o.get('notch_count',0)>=1 for o in rocks) for side in ['front','rear','left','right'])
checks['varied_notch_depths']=len({round(o.get('max_notch_depth',0),3) for o in rocks})>10
checks['retained_inner_shell']=len([o for o in bpy.data.objects if o.name.startswith('Interior wall')])==4
checks['ridge_crevasses']=any(o.get('crevasse_count',0)>=3 for o in bpy.data.objects)
checks['river_cross_section']=any(o.name.startswith('River / depth') for o in bpy.data.objects)
checks['portable_fine_maps']=any(i.size[0]==512 and i.packed_file for i in bpy.data.images)
checks['lid_attachments']=all(o.parent and o.parent.name=='Lid_Hinge' for o in bpy.data.objects if o.name.startswith(('River /','Glacier /')))
(R/('features-red.json' if '--baseline' in sys.argv else 'features-check.json')).write_text(json.dumps(checks,indent=2));print(checks);assert all(checks.values())
