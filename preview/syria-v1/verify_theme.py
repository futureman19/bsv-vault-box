import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'syria.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
def check():
 rosettes=[o for o in bpy.data.objects if o.name.startswith('Inlay / rosette')]
 borders=[o for o in bpy.data.objects if o.name.startswith('Inlay / lid border')]
 front=[o for o in bpy.data.objects if o.name.startswith('Inlay / front band')]
 assert (len(rosettes),len(borders),len(front))==(24,34,38)
 assert all(o.parent==lid for o in rosettes+borders),'detached lid ornament'
 zs=[(o.matrix_world@v.co).z for o in rosettes+borders for v in o.data.vertices]
 assert min(zs)>=1.978 and max(zs)<=2.08
 assert not any(o.name.startswith(('Cedar tree','Terrain / moss')) for o in bpy.data.objects)
 return {'rosette_lozenges':len(rosettes),'lid_border_diamonds':len(borders),'front_diamonds':len(front),'ornament_z':[min(zs),max(zs)]}
r=check();o=next(o for o in bpy.data.objects if o.name.startswith('Inlay / rosette'));o.parent=None
try:check()
except AssertionError as e:r['detached_ornament_negative_control']=str(e)
else:raise AssertionError('Negative control unexpectedly passed')
r['status']='PASS';r['negative_control_scope']='In-memory only; source not saved';(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
