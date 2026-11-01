from pathlib import Path
import struct,json,sys
R=Path(__file__).resolve().parent
p=Path(sys.argv[1]) if len(sys.argv)>1 else R/'iceland.glb'
b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);checks={}
m=next(m for m in g['materials'] if m['name']=='Glacier / blue depth');e=m.get('extensions',{})
checks['portable_glass_transmission']=e.get('KHR_materials_transmission',{}).get('transmissionFactor',0)>=.8
checks['portable_glass_roughness']=m['pbrMetallicRoughness'].get('roughnessFactor',1)<.12
checks['portable_volume_thickness']=e.get('KHR_materials_volume',{}).get('thicknessFactor',0)>.1
checks['portable_ior']=abs(e.get('KHR_materials_ior',{}).get('ior',1.5)-1.31)<.001
rock=[m for m in g['materials'] if m['name'].startswith('Basalt /')]
checks['rock_luminance_multiplier']=all(max(m['pbrMetallicRoughness'].get('baseColorFactor',[1])[:3])<.4 for m in rock)
checks['four_corner_top_wraps']=sum(n.get('name','').startswith('Corner strap / folded top') for n in g['nodes'])==4
checks['eight_new_top_rivets']=sum(n.get('name','').startswith('Corner cap / top rivet') for n in g['nodes'])==8
print(json.dumps({'asset':str(p),'checks':checks,'glacier_material':m},indent=2));assert all(checks.values()),checks
