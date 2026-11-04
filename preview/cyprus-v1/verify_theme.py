import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
base={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'cyprus.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];diamonds=[o for o in bpy.data.objects if o.name.startswith('Cutwork diamond')]
if '--negative' in sys.argv:diamonds[0].parent=None
try:
 assert len(diamonds)==12
 assert all(o.parent==lid for o in diamonds),'Detached cutwork ornament'
 for n,m in base.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
 verts=[o.matrix_world@v.co for o in diamonds for v in o.data.vertices]
 zmin=min(v.z for v in verts);zmax=max(v.z for v in verts)
 assert 2.0049<=zmin<2.007 and 2.045<zmax<2.075,(zmin,zmax)
 carrier=bpy.data.objects['Cutwork / inset carrier'];cv=[carrier.matrix_world@v.co for v in carrier.data.vertices];ctop=max(v.z for v in cv)
 assert zmin<=ctop+.0001,'Unseated threads'
 rays=[]
 for x in [-1.02,0,1.02]:
  for y in [-.43,.43]:
   hit,loc,no,idx,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
   assert hit and o.name==carrier.name,(x,y,o.name)
   rays.append([x,y,o.name,loc.z])
 assert len([o for o in bpy.data.objects if o.name.startswith('Linen body /')])==4
 assert not any(o.name.startswith(('Cedar','Terrain','Finger /')) for o in bpy.data.objects)
 result=dict(status='PASS',diamonds=6,diamond_meshes=12,relief_z=[zmin,zmax],carrier_top=ctop,open_center_rays=rays,original_pivots=True,all_ornaments_lid_parented=True)
except AssertionError as e:
 (R/('negative-control.json' if '--negative' in sys.argv else 'theme-check-failure.json')).write_text(json.dumps({'status':'EXPECTED_FAIL' if '--negative' in sys.argv else 'FAIL','reason':str(e)},indent=2));raise
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
