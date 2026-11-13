import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'comoros.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert tuple(round(v,3) for v in lid.location)==(0,1.32,1.668),tuple(lid.location)
orn=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Karthala /','Ylang /','Vegetation /'))]
assert all(o.parent==lid for o in orn)
petals=[o for o in orn if o.name.startswith('Ylang / petal')];assert len(petals)==18
crater=bpy.data.objects['Karthala / recessed crater'];bpy.context.view_layer.update();vs=[crater.matrix_world@v.co for v in crater.data.vertices]
center=vs[0].z;rim=max(v.z for v in vs);assert rim-center>.25 and rim-1.978<.65
assert max(v.x for v in vs)-min(v.x for v in vs)>2
assert not any(o.name.startswith(('Cedar','Finger','Glacier','River')) for o in bpy.data.objects)
assert all(o.dimensions.z<=.101 for o in bpy.data.objects if o.name.startswith('Ocean seam'))
imgs=[i for i in bpy.data.images if i.packed_file];assert len(imgs)==3 and all(max(i.size)<=512 for i in imgs)
r={'status':'PASS','ornaments_on_lid':len(orn),'petals':len(petals),'crater_center_z':center,'crater_rim_z':rim,'maps':[i.name for i in imgs],'pivot':list(lid.location)}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
