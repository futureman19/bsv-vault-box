"""Burundi: original coiled-fibre interpretation on inherited mechanism."""
import bpy,math,json,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'helpers.py').read_text())
wood=mat('Frame / smoked brown',(.075,.036,.017),.62)
fibre=mat('Sisal / original woven diamonds',(.56,.39,.19),.8)
maptex(fibre,'sisal-color.png','Base Color');maptex(fibre,'sisal-roughness.png','Roughness',True)
t=fibre.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/sisal-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack()
n=fibre.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.35;fibre.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);fibre.node_tree.links.new(n.outputs['Normal'],fibre.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
straw=mat('Sweetgrass / pale gold',(.56,.38,.16),.87)
charcoal=mat('Dyed fibre / charcoal',(.045,.029,.018),.9)
brick=mat('Dyed fibre / brick',(.29,.075,.036),.9)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
# Four solid skins with fine woven map; world-local face UV, not stretching side panels.
for sy in [-1,1]:
 o=cube('Woven panel / front' if sy<0 else 'Woven panel / rear',(0,sy*1.145,.83),(3.72,.19,1.46),fibre,bevel=.015)
 for poly in o.data.polygons:
  for li in poly.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.x/3.72+.5,co.z/1.46+.5)
for sx in [-1,1]:
 o=cube('Woven panel / side',(sx*1.745,0,.83),(.23,2.48,1.46),fibre,bevel=.015)
 for poly in o.data.polygons:
  for li in poly.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.y/2.48+.5,co.z/1.46+.5)
for z in [.135,1.515]:
 for sy in [-1,1]:cube('Frame / long binding',(0,sy*1.246,z),(3.72,.035,.07),wood,bevel=.012)
 for sx in [-1,1]:cube('Frame / end binding',(sx*1.871,0,z),(.035,2.48,.07),wood,bevel=.012)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Frame / corner binding',(sx*1.755,sy*1.25,.83),(.20,.045,1.46),wood,bevel=.01)
  cube('Foot / smoked timber',(sx*1.47,sy*.91,-.10),(.46,.39,.30),wood,bevel=.07)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Reveal / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),charcoal,bevel=.009)
for sx in [-1,1]:
 cube('Reveal / side',(sx*1.74,0,1.618),(.16,2.05,.108),charcoal,bevel=.009)
 for sy in [-1,1]:cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
cube('Lid / woven inset',(0,0,1.984),(3.36,2.04,.022),fibre,lid,.006)
# Shallow raised nested oval coil study. Tiny modulation reads like bindings.
for k in range(17):
 a=1.35-k*.071;b=.80-k*.039
 pts=[]
 for j in range(193):
  angle=math.tau*j/192;pts.append((a*math.cos(angle),b*math.sin(angle),2.035+.012*math.sin(k*.7)))
 material=charcoal if k in [3,4,10,11] else brick if k in [6,13] else straw
 tube('Lid coil / %02d'%k,pts,[.0265]*len(pts),material,lid,sides=6)
# Solid central weave button, no sacred or invented insignia.
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=8,radius=1,location=(0,0,2.025));o=bpy.context.object;o.name='Lid coil / centre';o.scale=(.17,.14,.045);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(straw);parent(o)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
exec((R/'finish.py').read_text())
