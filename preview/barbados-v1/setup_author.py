from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('wood=mat')]+'''wood=mat('Coral limestone / porous ivory',(.65,.57,.40),.72);maptex(wood,'limestone-color.png','Base Color');maptex(wood,'limestone-roughness.png','Roughness',True)
t=wood.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/limestone-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=wood.node_tree.nodes.new('ShaderNodeNormalMap');wood.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);wood.node_tree.links.new(n.outputs['Normal'],wood.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
granite=wood
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / dark teal',(.018,.065,.061),.8)
water=mat('Coast / turquoise enamel',(.015,.36,.37),.23,.12)
'''+s[s.index('def uv('):s.index('# Exterior skins')]+'''for sy in [-1,1]:cube('Limestone / front rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Limestone / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025)
'''+s[s.index('# Small collar'):s.index('# A thin satin')]+s[s.index('# Restrained brass'):s.index('stone(\'Terrain / granite')]+'''# Original low coastal relief. Closed irregular terrace prisms, not a glacier.
def terrace(name,cx,cy,rx,ry,bottom,top,material):
 count=40;vs=[]
 for z in [bottom,top]:
  for j in range(count):
   a=j*math.tau/count;k=1+.07*math.sin(a*5)+.035*math.cos(a*9)
   vs.append((cx+rx*k*math.cos(a),cy+ry*k*math.sin(a),z))
 fs=[tuple(reversed(range(count))),tuple(range(count,2*count))]
 for j in range(count):k=(j+1)%count;fs.append((j,k,k+count,j+count))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
terrace('Coast / turquoise inlay',-.20,-.12,1.35,.77,1.975,2.015,water)
terrace('Terrace / lower',.30,.24,1.10,.60,1.98,2.16,wood)
terrace('Terrace / middle',.48,.31,.77,.42,2.15,2.32,wood)
terrace('Terrace / upper',.62,.38,.43,.25,2.31,2.49,wood)
'''+s[s.index('# Medallion'):]
s=s.replace('Cedar /','Limestone /').replace('Granite foot','Limestone foot').replace('japan.blend','barbados.blend').replace('japan.glb','barbados.glb').replace('JAPAN AUTHORED','BARBADOS AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=1000').replace('resolution_y=1000','resolution_y=850')
a=s.index('def uv(');b=s.index('def cube(',a)
s=s[:a]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda k:abs(p.normal[k]));axes=[k for k in range(3) if k!=axis]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]/1.8+.5,co[axes[1]]/1.8+.5)
'''+s[b:]
s=s.replace('Reference-led Japan pilot.','Brief-led Barbados pilot.')
(R/'author.py').write_text(s)
print('author script generated')
