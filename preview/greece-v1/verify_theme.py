import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'greece.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert latch.parent==lid
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Fanlight /','Inlay /'))]
assert len(ornaments)==14 and all(o.parent==lid for o in ornaments)
ribs=[o for o in ornaments if 'radial rib' in o.name];assert len(ribs)==7
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
source_pivots={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
gaps=[]
for i in range(6):
 a=(i+1.5)*math.pi/8;x=.48*math.cos(a);y=-.20+.48*math.sin(a)
 hit,loc,normal,idx,obj,mat=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and obj.name=='Lid / polished slab',(i,obj.name)
 gaps.append({'x':x,'y':y,'hit':obj.name,'z':loc.z})
for o in ribs:
 c=o.matrix_world.translation;hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((c.x,c.y,3)),Vector((0,0,-1)))
 assert obj==o and loc.z>2.07
verts=[o.matrix_world@v.co for o in ornaments if o.name.startswith('Fanlight') for v in o.data.vertices]
assert min(v.z for v in verts)>=1.977 and max(v.z for v in verts)<=2.10
# Actual detached ornament negative control, checked by same ownership invariant.
ribs[0].parent=None
negative_rejected=not all(o.parent==lid for o in ornaments);assert negative_rejected
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,matrix in source_pivots.items():assert max(abs(matrix[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6
out={'status':'PASS','ribs':7,'openwork_gap_rays':gaps,'ornaments_lid_owned':14,'detached_ornament_negative_control_rejected':negative_rejected,'original_pivots_unchanged':True,'relief_z':[min(v.z for v in verts),max(v.z for v in verts)],'interpretation':'Openwork relief over solid lid, not pierced container.'}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
