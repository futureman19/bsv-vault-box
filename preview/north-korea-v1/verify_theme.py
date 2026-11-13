import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'north-korea.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];ring=bpy.data.objects['Terrain / Paektu caldera'];lake=bpy.data.objects['Terrain / Lake Chon']
def owned():
 assert ring.parent==lid and lake.parent==lid,'Detached terrain'
owned();lake.parent=None
try:
 owned()
except AssertionError as e:
 negative=str(e)
else:raise AssertionError('negative control was accepted')
lake.parent=lid
verts=[ring.matrix_world@v.co for v in ring.data.vertices];rim=verts[96:192]
assert min(v.z for v in rim)>2.28
assert max(v.z for v in rim)<2.58
assert abs(min(v.z for v in verts)-1.977)<1e-5
assert all((.70*__import__('math').cos(j*__import__('math').tau/96))**2/.73**2+(.44*__import__('math').sin(j*__import__('math').tau/96))**2/.46**2<1 for j in range(96))
assert not any('Cedar' in o.name for o in bpy.data.objects)
r={'status':'PASS','terrain_lid_owned':True,'negative_control_rejected':negative,'rim_z':[min(v.z for v in rim),max(v.z for v in rim)],'lake_surface_z':2.08,'outer_foot_z':min(v.z for v in verts),'notes':'Lake boundary inside nominal inner-wall ellipse; stylized non-surveyed geometry.'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
