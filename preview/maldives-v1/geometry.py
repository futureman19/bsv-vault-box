wood=mat('Sand / coralline mineral',(.73,.65,.46),.72);maptex(wood,'sand-color.png','Base Color');maptex(wood,'sand-roughness.png','Roughness',True)
t=wood.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/sand-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();nn=wood.node_tree.nodes.new('ShaderNodeNormalMap');nn.inputs['Strength'].default_value=.18;wood.node_tree.links.new(t.outputs['Color'],nn.inputs['Color']);wood.node_tree.links.new(nn.outputs['Normal'],wood.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
granite=wood;gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
ocean=mat('Ocean / deep teal enamel',(.009,.08,.10),.22,.12)
lagoon=mat('Lagoon / turquoise enamel',(.028,.43,.39),.25,.05)
green=mat('Cays / coastal green',(.075,.19,.065),.85)
seam=mat('Seam / deep teal',(.018,.045,.04),.8)
# HELPERS
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Sand / front or rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.028)
for sx in [-1,1]:cube('Sand / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.028)
cube('Sand / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Sand / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),ocean,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def mesh(n,v,f,m):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(m);uv(o);parent(o);return o
# Open-ended annular solid, sand channel at +X. Top winding points up.
v=[];f=[];N=80
for i in range(N+1):
 a=.13+(math.tau-.26)*i/N;k=1+.025*math.sin(5*a)+.018*math.cos(9*a)
 for rx,ry,z in [(1.42,.84,1.979),(1.42,.84,2.065+.035*math.sin(a*3)**2),(.99,.51,2.045),(.99,.51,1.979)]:v.append((rx*k*math.cos(a),ry*k*math.sin(a),z))
for i in range(N):
 a=i*4;b=a+4
 f.extend([(a,b,b+1,a+1),(a+1,b+1,b+2,a+2),(a+2,b+2,b+3,a+3),(a+3,b+3,b,a)])
f.extend([(0,1,2,3),(N*4+3,N*4+2,N*4+1,N*4)])
mesh('Faro / raised sand reef',v,f,wood)
# Lagoon lies inside inner shoreline; flat enamel interpretation, not transmission water.
v=[(0,0,2.01)]+[(.97*math.cos(i*math.tau/80),.495*math.sin(i*math.tau/80),2.01) for i in range(80)]
mesh('Lagoon / inset',v,[(0,i+1,(i+1)%80+1) for i in range(80)],lagoon)
for i,a in enumerate([1.1,2.9,4.4]):
 x=1.19*math.cos(a);y=.68*math.sin(a)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,radius=1,location=(x,y,2.087));o=bpy.context.object;o.name='Cay / vegetation '+str(i);o.scale=(.20,.105,.075);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(green);parent(o)
 for face in o.data.polygons:face.use_smooth=True
