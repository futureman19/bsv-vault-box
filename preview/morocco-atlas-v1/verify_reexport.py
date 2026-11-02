import bpy,json,hashlib,os
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'morocco.blend'),use_scripts=False)
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Lid_Hinge']
p=Path(os.environ.get('TMPDIR',str(R)))/'morocco-independent-reexport.glb'
bpy.ops.export_scene.gltf(filepath=str(p),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
a=hashlib.sha256((R/'morocco.glb').read_bytes()).hexdigest();b=hashlib.sha256(p.read_bytes()).hexdigest()
result={'saved_source_reopened':True,'reexport_bytes':p.stat().st_size,'delivered_sha256':a,'reexport_sha256':b,'byte_identical':a==b}
# Saving/reopening Blender rounds UVs by a few float32 ULPs; diagnose,
# never waive geometry/material/image differences under a blanket hash rule.
import struct,numpy as np
rawa=(R/'morocco.glb').read_bytes();rawb=p.read_bytes()
na=struct.unpack_from('<I',rawa,12)[0];nb=struct.unpack_from('<I',rawb,12)[0]
da=json.loads(rawa[20:20+na]);db=json.loads(rawb[20:20+nb]);assert da==db
ba=rawa[28+na:];bb=rawb[28+nb:];uv_ids={prim['attributes']['TEXCOORD_0'] for mesh in da['meshes'] for prim in mesh['primitives'] if 'TEXCOORD_0' in prim['attributes']};changed=[]
for i,ac in enumerate(da['accessors']):
 bv=da['bufferViews'][ac['bufferView']];off=bv.get('byteOffset',0)+ac.get('byteOffset',0);count=ac['count']*{'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[ac['type']];dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[ac['componentType']]
 va=np.frombuffer(ba,dtype=dt,count=count,offset=off);vb=np.frombuffer(bb,dtype=dt,count=count,offset=off)
 if not np.array_equal(va,vb):
  delta=float(np.max(np.abs(va-vb)));assert i in uv_ids and delta<1e-6;changed.append({'accessor':i,'UV_max_delta':delta})
for image in da['images']:
 bv=da['bufferViews'][image['bufferView']];lo=bv.get('byteOffset',0);hi=lo+bv['byteLength'];assert ba[lo:hi]==bb[lo:hi]
result.update({'json_identical':True,'positions_normals_indices_images_exact':True,'UV_roundtrip_tolerance':1e-6,'changed_UV_accessors':changed})
(R/'reexport-check.json').write_text(json.dumps(result,indent=2));print(result)
p.unlink()
