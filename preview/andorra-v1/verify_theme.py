import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'andorra.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
orn=[o for o in bpy.data.objects if o.name.startswith(('Terrain /','Path /'))]
if '--negative' in sys.argv:orn[0].parent=None
assert len(orn)==18,len(orn)
assert all(o.parent and o.parent.name=='Lid_Hinge' for o in orn),'Detached ornament rejected'
assert len([o for o in bpy.data.objects if o.name.startswith('Masonry /')])==80
verts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
assert max(v.z for v in verts)<2.8 and min(v.z for v in verts)>=1.974
assert all(abs(v.x)<1.45 and abs(v.y)<.86 for v in verts)
hits=[]
for j in range(15):
 x=.08*math.sin(j*.45);y=-.76+j*.108
 hit,loc,n,idx,obj,mat=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and obj.name.startswith('Path /'),(j,obj.name if obj else None)
 hits.append({'point':[x,y],'hit':obj.name,'z':loc.z})
r={'status':'PASS','original_pivots':True,'lid_ornaments':len(orn),'masonry_blocks':80,'summit_z':max(v.z for v in verts),'path_visibility_rays':hits,'interpretation':'stylized, not a geographic reconstruction'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS')
