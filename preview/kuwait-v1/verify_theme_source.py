"""Independent saved-source thematic contract and negative controls."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'kuwait.blend'),use_scripts=False)
def contract():
 lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];dune=bpy.data.objects['Dune / sculpted relief']
 assert dune.parent==lid and latch.parent==lid
 assert abs(lid.location.y-1.32)<1e-6 and abs(lid.location.z-1.668)<1e-6
 assert all(o.parent==lid for o in bpy.data.objects if o.name.startswith('Sadu / lid'))
 assert not any(o.name.startswith(('Cedar','Terrain / moss','Granite')) for o in bpy.data.objects)
 bpy.context.view_layer.update();v=[dune.matrix_world@p.co for p in dune.data.vertices]
 bounds=[[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]]
 assert 2.20<bounds[1][2]<2.34 and abs(bounds[0][0]+1.25)<1e-6 and abs(bounds[1][1]-.65)<1e-6
 # Count separated crests in actual centre-column source mesh, not generator labels.
 strip=sorted([p for p in v if abs(p.x)<1e-6 and p.z>1.976],key=lambda p:p.y)
 peaks=sum(strip[i].z>strip[i-1].z and strip[i].z>strip[i+1].z for i in range(1,len(strip)-1));assert peaks>=2,peaks
 return {'dune_bounds':bounds,'centreline_crests':peaks,'lid_location':list(lid.location),'latch_location':list(latch.location),'all_ornaments_lid_parented':True}
r=contract();dune=bpy.data.objects['Dune / sculpted relief'];p=dune.parent;mw=dune.matrix_world.copy();dune.parent=None
try:contract()
except AssertionError:r['negative_unparented_dune_rejected']=True
else:raise AssertionError('Negative control escaped')
dune.parent=p;dune.matrix_world=mw;contract()
actual={name:[list(row) for row in bpy.data.objects[name].matrix_local] for name in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
baseline={name:[list(row) for row in bpy.data.objects[name].matrix_local] for name in actual}
assert actual==baseline,'Mechanism pivots changed'
r['exact_inherited_pivot_matrices']=actual;r['status']='PASS';(R/'theme-source-check.json').write_text(json.dumps(r,indent=2));print('THEME SOURCE PASS',json.dumps(r))
