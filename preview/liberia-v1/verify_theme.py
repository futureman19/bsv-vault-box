import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'liberia.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge']
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Broadleaf /','Terrain /','River /'))]
assert len(ornaments)>=30
assert all(o.parent==lid for o in ornaments)
assert len([o for o in ornaments if o.name.startswith('Broadleaf / trunk')])==3
assert len([o for o in ornaments if o.name.startswith('Broadleaf / crown')])==15
river=bpy.data.objects['River / continuous ribbon'];assert len(river.data.vertices)==132
assert max(v.co.x for v in river.data.vertices)-min(v.co.x for v in river.data.vertices)>.5
assert all((o.matrix_world@v.co).z<2.9 for o in ornaments for v in o.data.vertices)
assert abs(bpy.data.objects['Lid / polished slab'].dimensions.x-3.72)<.01
assert all(i.packed_file for i in bpy.data.images if i.name.endswith('.png'))
result={'status':'PASS','theme':'Sapo Rainforest & River','lid_ornaments':len(ornaments),'broadleaf_trees':3,'crown_clusters':15,'river_vertices':132,'ornament_parentage':True,'height_under_2_9':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
