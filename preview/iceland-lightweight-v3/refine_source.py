"""Reopen original editable source; only UV/material edits. No geometry changes."""
import bpy
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'original/iceland.blend'),use_scripts=False)
for o in bpy.data.objects:
 if o.type!='MESH' or not o.name.startswith('Basalt column'):continue
 uv=o.data.uv_layers.new(name='BasaltUV')
 for poly in o.data.polygons:
  nx,ny,nz=poly.normal
  for li in poly.loop_indices:
   x,y,z=o.data.vertices[o.data.loops[li].vertex_index].co
   u,v=(-y,z) if abs(nx)>abs(ny) else (x,z)
   if abs(nz)>max(abs(nx),abs(ny)):u,v=x,-y
   uv.data[li].uv=(u*2,v*2)
for m in bpy.data.materials:
 if not m.name.startswith('Basalt /'):continue
 nodes=m.node_tree.nodes;links=m.node_tree.links;p=nodes.get('Principled BSDF');color=tuple(p.inputs['Base Color'].default_value);rf=p.inputs['Roughness'].default_value
 def tex(name,noncolor=False):
  t=nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'textures'/name),check_existing=True)
  if noncolor:t.image.colorspace_settings.name='Non-Color'
  t.image.pack();return t
 t=tex('basalt-color.jpg');mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=color;links.new(t.outputs['Color'],mix.inputs[1]);links.new(mix.outputs[0],p.inputs['Base Color'])
 t=tex('basalt-orm.jpg',True);sep=nodes.new('ShaderNodeSeparateColor');links.new(t.outputs['Color'],sep.inputs[0]);mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=rf;links.new(sep.outputs['Green'],mul.inputs[0]);links.new(mul.outputs[0],p.inputs['Roughness'])
 t=tex('basalt-normal.png',True);n=nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.35;links.new(t.outputs['Color'],n.inputs['Color']);links.new(n.outputs[0],p.inputs['Normal'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'iceland.blend'))
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
