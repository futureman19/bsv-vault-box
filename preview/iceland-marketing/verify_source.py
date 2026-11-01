import bpy,json,struct,hashlib,math
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parent;S=R.parent/'iceland-lightweight-v3'
b=(S/'iceland.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);binary=b[28+n:]
bpy.ops.wm.open_mainfile(filepath=str(S/'iceland.blend'),use_scripts=False)
matched=[]
for m in g['materials']:
 material=bpy.data.materials[m['name']];p=material.node_tree.nodes.get('Principled BSDF');pbr=m['pbrMetallicRoughness']
 # Factor comparison: basalt linked inputs retain original authored multiplier.
 for a,c in zip(p.inputs['Base Color'].default_value,pbr.get('baseColorFactor',[1]*4)):assert abs(a-c)<1e-6
 assert abs(p.inputs['Metallic'].default_value-pbr.get('metallicFactor',1))<1e-6
 assert abs(p.inputs['Roughness'].default_value-pbr.get('roughnessFactor',1))<1e-6
 matched.append(m['name'])
for image in g['images']:
 v=g['bufferViews'][image['bufferView']];raw=binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
 assert raw==(S/'textures'/image['name']).read_bytes()
 assert raw==bytes(bpy.data.images[image['name']].packed_file.data)
def snapshot():
 out={}
 for o in bpy.data.objects:
  if o.type!='MESH' or o.name.startswith('Studio'):continue
  out[o.name]={'verts':[list(v.co) for v in o.data.vertices],'polys':[list(p.vertices) for p in o.data.polygons],'materials':[m.name for m in o.data.materials],'uv':[[list(x.uv) for x in uv.data] for uv in o.data.uv_layers],'parent':o.parent.name if o.parent else None}
 return out
baseline=snapshot();checks=[]
for name,lid,latch in [('01-closed-hero',0,0),('02-open-hero',-105,-80),('03-material-macro',0,0)]:
 bpy.ops.wm.open_mainfile(filepath=str(R/(name+'.blend')),use_scripts=False)
 assert snapshot()==baseline
 assert abs(bpy.data.objects['Lid_Hinge'].rotation_euler.x-math.radians(lid))<1e-6
 assert abs(bpy.data.objects['Latch_Pivot'].rotation_euler.x-math.radians(latch))<1e-6
 bpy.context.view_layer.update();scene=bpy.context.scene;points=[]
 for o in scene.objects:
  if o.name not in baseline:continue
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
  points.extend(world_to_camera_view(scene,scene.camera,ev.matrix_world@v.co) for v in mesh.vertices);ev.to_mesh_clear()
 bounds=[min(p.x for p in points),min(p.y for p in points),max(p.x for p in points),max(p.y for p in points)]
 if name!='03-material-macro':assert min(bounds[:2])>.05 and max(bounds[2:])<.95
 checks.append({'shot':name,'reopened_mesh_uv_material_assignments_equal_source':True,'endpoint_pose_verified':True,'projected_silhouette_bounds':bounds,'crop_intentional':name=='03-material-macro'})
result={'glb_source_material_factors_match':matched,'all_three_embedded_texture_bytes_match_source_packed_images':True,'shots':checks}
(R/'source-parity-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
