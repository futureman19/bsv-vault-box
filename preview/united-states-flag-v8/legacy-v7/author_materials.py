"""Reopen packed V6; only lid UVs and two paint images change. No geometry edits."""
import bpy,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline-v6.blend'),use_scripts=False)
for name in ['flag-lid.png','flag-wall.png']:
 im=bpy.data.images.get(name);im.unpack(method='REMOVE');im.filepath=str(R/'maps'/name);im.reload();im.pack()
bpy.context.view_layer.update()
o=bpy.data.objects['Lid / polished slab'];uv=o.data.uv_layers.active
radius=.045;segment=2*radius*math.sin(math.pi/12);arc=3*segment
# Each existing bevel chord receives its actual physical developed length.
def developed(out,z):
 if z>=1.933-1e-6:
  angle=math.atan2(max(0,out),max(0,z-1.933))
  return angle/(math.pi/6)*segment
 return arc+1.933-z
for p in o.data.polygons:
 for li in p.loop_indices:
  co=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
  x,y=co.x,co.y
  if p.normal.z<-.999:
   # Underside perimeter is developed past the entire lid thickness, not reset
   # to the top atlas: resetting would echo clipped edge stars at the lower seam.
   x=math.copysign(1.815+arc+1.933-co.z,x)
   y=math.copysign(1.145+arc+1.933-co.z,y)
  else:
   if x< -1.815+1e-6 and abs(p.normal.x)>1e-5:x=-1.815-developed(-x-1.815,co.z)
   elif x>1.815-1e-6 and abs(p.normal.x)>1e-5:x=1.815+developed(x-1.815,co.z)
   if y< -1.145+1e-6 and abs(p.normal.y)>1e-5:y=-1.145-developed(-y-1.145,co.z)
   elif y>1.145-1e-6 and abs(p.normal.y)>1e-5:y=1.145+developed(y-1.145,co.z)
  uv.data[li].uv=((x+2.56)/5.12,(y+1.89)/3.78)
scene=bpy.context.scene;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4
bpy.ops.wm.save_as_mainfile(filepath=str(R/'united-states.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.objects:
 if not ob.name.startswith('Studio') and ob.type in ['MESH','EMPTY']:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Lid_Hinge']
bpy.ops.export_scene.gltf(filepath=str(R/'united-states.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'blender-source-no-fx.png');bpy.ops.render.render(write_still=True)
print('V7 packed source and export authored; geometry/mechanism unchanged')
