import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'italy.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];petals=[o for o in bpy.data.objects if o.name.startswith('Inlay / petal')];leaves=[o for o in bpy.data.objects if o.name.startswith('Inlay / leaf')]
if '--negative' in sys.argv:petals[0].parent=None
checks={}
checks['eight_petals']=len(petals)==8;checks['eight_leaves']=len(leaves)==8
orn=[o for o in bpy.data.objects if o.name.startswith('Inlay /')];checks['all_ornaments_lid_owned']=all(o.parent==lid for o in orn)
verts=[o.matrix_world@v.co for o in petals+leaves for v in o.data.vertices];checks['relief_seated']=all(1.9769<=v.z<=2.0151 for v in verts)
# Independent rays show petal centers above the slab and an empty area reaching slab.
dep=bpy.context.evaluated_depsgraph_get()
def ray(x,y):
 hit,loc,n,i,o,m=bpy.context.scene.ray_cast(dep,Vector((x,y,3)),Vector((0,0,-1)));return o.name if hit else None
checks['petal_exposed']=ray(.43,0)=='Inlay / petal 0';checks['negative_space_exposed']=ray(0,.78)=='Lid / polished slab'
checks['stone_skin_count']=len([o for o in bpy.data.objects if o.name.startswith('Stone skin')])==4
checks['no_old_theme']=not any(o.name.startswith(('Cedar','Terrain','Finger')) for o in bpy.data.objects)
checks['lid_dimensions']=all(abs(a-b)<1e-5 for a,b in zip(bpy.data.objects['Lid / polished slab'].dimensions,(3.72,2.38,.30)))
r={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'ornaments':len(orn),'min_z':min(v.z for v in verts),'max_z':max(v.z for v in verts),'negative_control':'detached first petal' if '--negative' in sys.argv else None}
(R/('theme-negative.json' if '--negative' in sys.argv else 'theme-check.json')).write_text(json.dumps(r,indent=2));print(json.dumps(r));assert all(checks.values()),checks
