from pathlib import Path
import json
R=Path(__file__).resolve().parent
prefix,helpers,tail=json.loads((R/'author-parts.json').read_text())
body='''
wood=mat('Lacquer / black vermilion yun-inspired',(.04,.01,.008),.25);maptex(wood,'lacquer-color.png','Base Color');maptex(wood,'lacquer-roughness.png','Roughness',True)
lining=mat('Lacquer / red interior',(.3,.03,.015),.3);maptex(lining,'lining.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Lacquer / dark red seam',(.07,.009,.005),.4)
'''
geometry='''
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(lining if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Lacquer / front rear skin',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.012)
for sx in [-1,1]:cube('Lacquer / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.012,axis='Y')
cube('Lacquer / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Lacquer seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Lacquer seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Lacquer / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
  cube('Lacquer / foot',(sx*1.47,sy*.91,-.09),(.48,.42,.30),seam,bevel=.055)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=1,depth=.06,location=(0,0,2.005));o=bpy.context.object;o.name='Ornament / vermilion oval';o.scale=(.73,.49,1);o.data.materials.append(lining);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);uv(o);parent(o)
for i,r in enumerate([.35,.52,.69]):
 bpy.ops.mesh.primitive_torus_add(major_segments=96,minor_segments=8,major_radius=r,minor_radius=.008,location=(0,0,2.038));o=bpy.context.object;o.name='Ornament / brass oval '+str(i);o.scale.y=.67;o.data.materials.append(gold);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);parent(o)
'''
(R/'author.py').write_text(prefix.replace('Reference-led Japan pilot','Brief-led Myanmar lacquer pilot')+body+helpers+geometry+tail,encoding='utf8')
