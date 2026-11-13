import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'france.blend'),use_scripts=False)
bpy.context.view_layer.update()
negative='--negative-control' in sys.argv
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
tiles=[o for o in bpy.data.objects if o.name.startswith('Glazed tile /')]
if negative:tiles[0].parent=None
checks={}
checks['160_individual_tile_meshes']=len(tiles)==160
checks['all_tiles_move_with_lid']=all(o.parent==lid for o in tiles)
coords=[o.matrix_world@v.co for o in tiles for v in o.data.vertices]
bounds=[[min(v[i] for v in coords),max(v[i] for v in coords)] for i in range(3)]
checks['tile_field_bounds']=bounds[0][0]>=-1.601 and bounds[0][1]<=1.601 and bounds[1][0]>=-.941 and bounds[1][1]<=.941
checks['raised_tile_top']=2.032<=bounds[2][1]<=2.045
checks['seated_tile_bottom']=1.997<=bounds[2][0]<=2.001
checks['four_glaze_colors']=len({o.active_material.name for o in tiles})==4
checks['glaze_roughness_metalness']=all(.219999<=o.active_material.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value<=.301 and o.active_material.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value==0 for o in tiles)
checks['original_lid_pivot']= (lid.location-Vector((0,1.32,1.668))).length<1e-5
checks['latch_owned_by_lid']=latch.parent==lid
# Independently compare source pivot transforms to frozen inherited mechanism.
pivot_snapshot={o.name:[list(row) for row in o.matrix_local] for o in [lid,latch]}
materials={o.active_material.name:list(o.active_material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value) for o in tiles}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
checks['inherited_pivots_exact']=all(max(abs(bpy.data.objects[n].matrix_local[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-6 for n,m in pivot_snapshot.items())
report={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'tile_world_bounds':bounds,'glaze_colors_linear':materials,'negative_control':negative}
(R/('theme-negative-control.json' if negative else 'theme-check.json')).write_text(json.dumps(report,indent=2))
print(json.dumps(report));assert all(checks.values()),'Theme checks failed'
