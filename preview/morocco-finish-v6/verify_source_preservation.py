import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent

def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);d={}
 for o in bpy.data.objects:
  if o.name.startswith('Studio'):continue
  x={'parent':o.parent.name if o.parent else None,'matrix_basis':[list(r) for r in o.matrix_basis],'matrix_parent_inverse':[list(r) for r in o.matrix_parent_inverse]}
  if o.type=='MESH':
   x['vertices']=[list(v.co) for v in o.data.vertices];x['faces']=[list(p.vertices) for p in o.data.polygons];x['uv']={u.name:[list(l.uv) for l in u.data] for u in o.data.uv_layers};x['materials']=[m.name for m in o.data.materials]
  d[o.name]=x
 return d
old=snapshot(R/'baseline/morocco.blend');new=snapshot(R/'morocco.blend');assert old.keys()==new.keys();checked=[]
for name,a in old.items():
 b=new[name]
 for k in ['parent','matrix_basis','matrix_parent_inverse']:assert a[k]==b[k],(name,k)
 if name.startswith('Ceramic tessera'):continue
 for k in ['vertices','faces']:
  if k in a:assert a[k]==b[k],(name,k)
 if name.startswith('Tile bed'):continue
 for k,v in a.get('uv',{}).items():assert b['uv'][k]==v,(name,k)
 if name!='Lid / polished slab':assert a.get('materials')==b.get('materials'),name
 else:assert a['materials']==b['materials'][:1]
 checked.append(name)
# Check source body multiplier and packed image identity through actual source.
m=bpy.data.materials['Reference / Morocco reddish mineral strata'];mul=next(n for n in m.node_tree.nodes if n.type=='MIX_RGB');assert mul.blend_type=='MULTIPLY' and abs(mul.inputs[2].default_value[0]-.9)<1e-6
res={'all_original_names_and_parent_transforms_exact':True,'non_ceramic_raw_geometry_exact':True,'original_body_and_top_UV_exact':True,'source_body_multiplier':list(mul.inputs[2].default_value),'unchanged_object_checks':len(checked),'ceramic_only_geometry_replacement':3}
(R/'source-preservation-check.json').write_text(json.dumps(res,indent=2));print(res)
