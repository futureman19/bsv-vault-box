"""One-time derivation of the proven mechanical authoring helpers."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('wood=mat')]+'''wood=mat('Pandanus / woven straw',(.55,.39,.19),.7);maptex(wood,'weave-color.png','Base Color');maptex(wood,'weave-roughness.png','Roughness',True)
t=wood.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/weave-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack()
n=wood.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.45;wood.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);wood.node_tree.links.new(n.outputs['Normal'],wood.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
end=mat('Border / dark red fibre',(.30,.075,.035),.8)
granite=mat('Coral sand / ivory',(.78,.66,.40),.83)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / deep brown',(.045,.025,.012),.9)
water=mat('Lagoon / turquoise',(.018,.39,.43),.24)
'''+s[s.index('def uv('):s.index('# Exterior skins')]+'''
# Planar woven cladding over an inherited continuous hollow liner.
for sy in [-1,1]:
 cube('Pandanus / woven face',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.008)
 for z in [.18,1.48]:cube('Fibre / red border',(0,sy*1.246,z),(3.70,.018,.075),end,bevel=.003)
for sx in [-1,1]:
 cube('Pandanus / woven side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.008,axis='Y')
 for z in [.18,1.48]:cube('Fibre / side border',(sx*1.867,0,z),(.018,2.10,.075),end,bevel=.003,axis='Y')
'''+s[s.index('# Small collar'):s.index('# A thin satin')]+s[s.index('# Restrained brass'):s.index('stone(\'Terrain')]+'''
# An original low elliptical coral-island relief, not a map of Funafuti.
# Closed sand footprint supports a shallow inset lagoon with visible sand rim.
N=72
outer=[(1.39*math.cos(i*math.tau/N)*(1+.035*math.sin(i*.8)),.80*math.sin(i*math.tau/N)*(1+.035*math.sin(i*.6))) for i in range(N)]
inner=[(.99*math.cos(i*math.tau/N)*(1+.04*math.sin(i*.8))+.04,.48*math.sin(i*math.tau/N)*(1+.04*math.sin(i*.6))) for i in range(N)]
def relief(name,xy,z,depth,material):
 verts=[(x,y,z-depth) for x,y in xy]+[(x,y,z) for x,y in xy]
 faces=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);return o
relief('Island / coral sand footprint',outer,2.055,.077,granite)
relief('Lagoon / contained turquoise inset',inner,2.065,.009,water)
# Woven lid corners remain visible around low relief.
'''+s[s.index('# Medallion'):]
s=s.replace('Cedar / clasp seat','Pandanus / clasp seat').replace('Cedar / rim corner','Pandanus / rim corner').replace('Granite foot','Coral sand foot').replace('Mineral seam','Dark seam')
s=s.replace("scene.cycles.samples=32","scene.cycles.samples=16;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False")
s=s.replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('japan.blend','tuvalu.blend').replace('japan.glb','tuvalu.glb').replace('JAPAN AUTHORED','TUVALU AUTHORED')
# Projection by dominant normal prevents side-face UV collapse.
a=s.index('   u=co.y');b=s.index('def cube',a)
s=s[:a]+'''   normal=p.normal
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/1.7+.5,v/1.7+.5)
'''+s[b:]
(R/'author.py').write_text(s)
