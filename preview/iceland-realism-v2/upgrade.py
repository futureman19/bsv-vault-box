"""Executed inside author.py after approved v1 geometry, before save/export."""
import hashlib
# Visible load path: fixed mounting ear reaches bearing; lid-side strap reaches slab.
for o in parts:
 if o.name.startswith('Hinge / fixed mount'):o.location.z+=.025
for x in [-1.13,1.13]:
 cube('Hinge / lid anchor strap',(x,1.11,1.67),(.28,.32,.045),brass,.008,lid)
 # Fasteners are part of the moving strap and remain inside the lid-side envelope.
 cyl('Hinge / strap rivet',(x,1.00,1.701),.026,.018,brass,parent=lid)
# Keep all pivots, cavity and swept clearances. Exterior-only subtle broken edges.
for o in parts:
 if o.name.startswith('Basalt column'):
  for v in o.data.vertices:
   # Mid-course edges only; bounds at rim and base retained.
   if .18<v.co.z<1.30:
    v.co.x+=random.uniform(-.009,.009);v.co.y+=random.uniform(-.009,.009)
  o.data.materials.clear();o.data.materials.append(stones[0])
  for p in o.data.polygons:p.material_index=0
  mod=o.modifiers.new('Small eroded stone arrises','BEVEL');mod.width=.009;mod.segments=2
  o.modifiers.new('Stone weighted normals','WEIGHTED_NORMAL')
# Material images and UVs are explicit, portable, and packed into source.
def pbr(m,f,metal):
 nodes=m.node_tree.nodes;links=m.node_tree.links;p=nodes.get('Principled BSDF')
 p.inputs['Metallic'].default_value=metal
 for kind,socket in [('color','Base Color'),('rough','Roughness'),('normal',None)]:
  im=bpy.data.images.load(str(ROOT/'textures'/f'{f}-{kind}.png'),check_existing=True)
  if kind!='color':im.colorspace_settings.name='Non-Color'
  im.pack();t=nodes.new('ShaderNodeTexImage');t.image=im;t.label=f'{f} / {kind} / procedural portable'
  if socket:links.new(t.outputs['Color'],p.inputs[socket])
  else:
   nm=nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.85 if f=='basalt' else .65
   links.new(t.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],p.inputs['Normal'])
pbr(stones[0],'basalt',0);pbr(obsidian,'lid',.08);pbr(brass,'brass',.82);pbr(inside,'interior',0)
p=blue.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.012,.045,.05,1);p.inputs['Emission Strength'].default_value=0;p.inputs['Roughness'].default_value=.42;p.inputs['Metallic'].default_value=.12
# UV projection from each surface's dominant axis, with per-object deterministic origin.
# World-sized texels avoid tiny rivets receiving the same full scratch pattern as the lid.
for o in parts:
 if o.type!='MESH':continue
 uv=o.data.uv_layers.active or o.data.uv_layers.new(name='SurfaceUV')
 digest=hashlib.sha256(o.name.encode()).digest();off=(digest[0]/255,digest[1]/255)
 family='basalt' if o.name.startswith('Basalt') else ('brass' if o.data.materials[0]==brass else 'other')
 density=.72 if family=='basalt' else .6
 for poly in o.data.polygons:
  ax=max(range(3),key=lambda i:abs(poly.normal[i]));axes=[i for i in range(3) if i!=ax]
  for li in poly.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   uv.data[li].uv=(co[axes[0]]*density+off[0],co[axes[1]]*density+off[1])
# Neutral product studio; tangible floor and large softboxes, not orange game lighting.
scene.cycles.samples=64
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.24,.27,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.35
for o in bpy.data.objects:
 if o.type=='LIGHT':
  o.data.color=(.95,.97,1) if 'key' in o.name else (1,.94,.84)
  if 'gold rim' in o.name:o.data.energy=850
scene.view_settings.exposure=.7
scene.render.film_transparent=False
scene.render.resolution_x=1500;scene.render.resolution_y=1200
# Floor contacts the feet at z=.02 rather than floating below them.
floor.location.z=0
bpy.context.preferences.filepaths.save_version=0
