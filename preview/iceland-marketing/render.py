"""Actual approved source, presentation-only. Run with Blender --background --python-exit-code 1 --python render.py."""
import bpy, math, json, hashlib, sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
SOURCE=R.parent/'iceland-lightweight-v3'
if '--' in sys.argv:
 args=sys.argv[sys.argv.index('--')+1:]
 if args: SOURCE=Path(args[0]).resolve()
R.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
protected={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
(R/'approved-hashes-before.json').write_text(json.dumps(protected,indent=2))
bpy.ops.wm.open_mainfile(filepath=str(SOURCE/'iceland.blend'),use_scripts=False)
scene=bpy.context.scene
# Keep every collectible datablock unchanged. Remove only original presentation.
for o in list(bpy.data.objects):
 if o.type in {'CAMERA','LIGHT'}: bpy.data.objects.remove(o,do_unlink=True)
assets=[o for o in scene.objects if not o.name.startswith('Studio /')]
def fingerprint():
 data={}
 for o in assets:
  if o.type=='MESH':
   data[o.name]={'vertices':[list(v.co) for v in o.data.vertices], 'polygons':[list(p.vertices) for p in o.data.polygons], 'materials':[m.name for m in o.data.materials], 'uv':[[list(x.uv) for x in uv.data] for uv in o.data.uv_layers]}
 for m in bpy.data.materials:
  if m.name.startswith('Studio'):continue
  data['material:'+m.name]={'nodes':[(n.name,n.bl_idname,[(i.name,list(i.default_value) if hasattr(i.default_value,'__len__') and not isinstance(i.default_value,str) else i.default_value) for i in n.inputs if hasattr(i,'default_value')]) for n in m.node_tree.nodes], 'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]}
 return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
asset_before=fingerprint()
scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True
scene.cycles.adaptive_threshold=.035
scene.cycles.max_bounces=8
backend='CPU'
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences
 prefs.compute_device_type='OPTIX';prefs.get_devices()
 gpu=[d for d in prefs.devices if d.type=='OPTIX']
 if gpu:
  for d in prefs.devices:d.use=d.type=='OPTIX'
  scene.cycles.device='GPU';backend='OPTIX '+', '.join(d.name for d in gpu)
except Exception as e: print('GPU fallback',e)
scene.render.resolution_x=3000;scene.render.resolution_y=3000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX';scene.view_settings.exposure=.25
scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.11,.13,.16,1)
scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.35
lights=[]
def area(name,loc,power,color,size,target=(0,0,1),size_y=None):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name='Marketing / '+name;o.data.energy=power;o.data.color=color;o.data.shape='RECTANGLE';o.data.size=size;o.data.size_y=size_y or size
 o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 lights.append({'name':name,'location':loc,'power_w':power,'color':color,'size':size,'size_y':size_y or size,'target':target})
area('large neutral key',(-3,-4,6),1250,(.93,.97,1),4.5,size_y=3)
area('soft front fill',(3,-5,3.3),700,(.87,.93,1),4)
area('neutral rim',(3,3,5),1500,(1,.94,.84),3,size_y=4)
area('lid strip',(-1,2,6),650,(1,1,1),4,size_y=1.2)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Marketing camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.lens=65
bpy.context.preferences.filepaths.save_version=0
shots=[{'name':'01-closed-hero','location':(5,-7,4.8),'target':(0,0,.9),'scale':5.7,'lid':0,'latch':0},
 {'name':'02-open-hero','location':(5,-8,5.3),'target':(0,.1,1.65),'scale':6.5,'lid':-105,'latch':-80},
 {'name':'03-material-macro','location':(4,-6,4.8),'target':(.75,-.62,1.31),'scale':2.65,'lid':0,'latch':0}]
for s in shots:
 bpy.data.objects['Lid_Hinge'].rotation_euler.x=math.radians(s['lid'])
 bpy.data.objects['Latch_Pivot'].rotation_euler.x=math.radians(s['latch'])
 cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=s['scale']
 bpy.context.view_layer.update()
 # Fit the complete evaluated open silhouette, including released latch.
 if s['name']=='02-open-hero':
  dep=bpy.context.evaluated_depsgraph_get();points=[];inverse=cam.matrix_world.inverted()
  for o in assets:
   if o.type!='MESH':continue
   ev=o.evaluated_get(dep);mesh=ev.to_mesh()
   points.extend(inverse @ (ev.matrix_world @ v.co) for v in mesh.vertices)
   ev.to_mesh_clear()
  xmin,xmax=min(p.x for p in points),max(p.x for p in points)
  ymin,ymax=min(p.y for p in points),max(p.y for p in points)
  shift=cam.rotation_euler.to_quaternion() @ Vector(((xmin+xmax)/2,(ymin+ymax)/2,0))
  cam.location+=shift;cam.data.ortho_scale=max(xmax-xmin,ymax-ymin)/.80
  s['fitted_location']=list(cam.location);s['fitted_scale']=cam.data.ortho_scale
  bpy.context.view_layer.update()
 assert fingerprint()==asset_before,'Collectible mesh/material modification'
 scene.render.filepath=str(R/(s['name']+'.png'))
 bpy.ops.wm.save_as_mainfile(filepath=str(R/(s['name']+'.blend')))
 bpy.ops.render.render(write_still=True)
protected_after={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
assert protected_after==protected
(R/'approved-hashes-after.json').write_text(json.dumps(protected_after,indent=2))
report={'blender':bpy.app.version_string,'backend':backend,'samples':64,'dimensions':[3000,3000],'asset_geometry_uv_material_fingerprint':asset_before,'asset_fingerprint_preserved_all_shots':True,'all_approved_files_byte_preserved':True,'source':str(SOURCE),'shots':shots,'lights':lights,'exposure':.25,'view_transform':'AgX','notes':'Original editable source with packed approved textures; no collectible material, geometry or texture edits. Open pose from motion.mjs endpoint: lid -105 deg, latch -80 deg. Studio floor retained from source; camera/lights/world changed.'}
(R/'render-provenance.json').write_text(json.dumps(report,indent=2))
print('MARKETING_RENDER_COMPLETE',json.dumps(report))
