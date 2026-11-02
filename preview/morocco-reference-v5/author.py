"""Modify ONLY body UV/material of the approved packed source; no mesh edits."""
import bpy,math,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R));from glb_tools import uv
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline/morocco.blend'),use_scripts=False)
body=[o for o in bpy.data.objects if o.name.startswith('Rose stone')]
m=body[0].data.materials[0];m.name='Reference / Morocco reddish mineral strata'
nt=m.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');p=nt.nodes.new('ShaderNodeBsdfPrincipled');nt.links.new(p.outputs['BSDF'],out.inputs['Surface']);p.inputs['Roughness'].default_value=.86

def image(name,non=False):
 n=nt.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/'maps'/name));n.image.colorspace_settings.name='Non-Color' if non else 'sRGB';n.image.pack();return n
c=image('reference-color.png');nt.links.new(c.outputs['Color'],p.inputs['Base Color'])
r=image('reference-orm.png',True);sep=nt.nodes.new('ShaderNodeSeparateColor');nt.links.new(r.outputs['Color'],sep.inputs[0]);nt.links.new(sep.outputs['Green'],p.inputs['Roughness'])
n=image('reference-normal.png',True);normal=nt.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.8;nt.links.new(n.outputs['Color'],normal.inputs['Color']);nt.links.new(normal.outputs['Normal'],p.inputs['Normal'])
for o in body:
 layer=o.data.uv_layers.active
 for loop in o.data.loops:
  v=o.matrix_world@o.data.vertices[loop.vertex_index].co
  layer.data[loop.index].uv=uv(v.x,v.y,v.z,'rear' in o.name)
# Remove orphaned body images only; preserve all used nonbody records.
for im in list(bpy.data.images):
 if not im.users:bpy.data.images.remove(im)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'morocco.blend'))
# Poster uses EXACT prior studio/camera/light configuration.
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('Saved body-only source and actual model poster')
