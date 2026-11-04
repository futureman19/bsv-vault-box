from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
head=s[s.index('import bpy'):s.index("wood=mat")]
utils=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
materials='''wood=mat('Walnut / warm rim',(.18,.08,.035),.48);maptex(wood,'walnut-color.png','Base Color')
weave=mat('Woven / charcoal burgundy',(.12,.05,.04),.85);maptex(weave,'weave-color.png','Base Color');maptex(weave,'weave-roughness.png','Roughness',True)
t=weave.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/weave-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=weave.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.25;weave.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);weave.node_tree.links.new(n.outputs['Normal'],weave.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / antique',(.48,.30,.10),.28,.8)
seam=mat('Seam / charcoal',(.022,.018,.014),.92)
red=mat('Petals / burgundy',(.24,.035,.06),.8)
ivory=mat('Petals / ivory',(.65,.50,.29),.8)
green=mat('Leaves / muted green',(.12,.18,.065),.85)
'''
body='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Four recessed woven panels with explicit panel-local UVs.
def panel(n,loc,dim,axis,p=None):
 o=cube(n,loc,dim,weave,p,bevel=.006)
 for poly in o.data.polygons:
  for li in poly.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.x/dim[0]+.5 if axis!='Y' else co.y/dim[1]+.5
   v=co.y/dim[1]+.5 if axis=='TOP' else co.z/dim[2]+.5
   o.data.uv_layers.active.data[li].uv=(u,v)
 return o
for sy in [-1,1]:
 cube('Walnut / wall',(0,sy*1.145,.83),(3.72,.19,1.46),wood)
 panel('Woven / wall',(0,sy*1.246,.83),(3.20,.012,1.10),'X')
for sx in [-1,1]:
 cube('Walnut / end',(sx*1.745,0,.83),(.23,2.10,1.46),wood,axis='Y')
 panel('Woven / end',(sx*1.866,0,.83),(.012,1.86,1.10),'Y')
 for sy in [-1,1]:cube('Walnut / corner',(sx*1.745,sy*1.145,.83),(.23,.19,1.46),wood)
cube('Walnut / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.08),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.08),seam,bevel=.009)
 for sy in [-1,1]:cube('Walnut / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
panel('Woven / lid',(0,0,1.986),(3.28,1.94,.016),'TOP',lid)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Walnut / foot',(sx*1.47,sy*.91,-.10),(.50,.42,.32),wood,bevel=.045)
# Raised eight-petal angular flowers, contemporary invention, not a copied textile.
def diamond(n,cx,cy,rx,ry,z,material,angle=0):
 pts=[(-rx,0),(0,-ry),(rx,0),(0,ry)];v=[]
 for zz in [z,z+.026]:
  for x,y in pts:v.append((cx+x*math.cos(angle)-y*math.sin(angle),cy+x*math.sin(angle)+y*math.cos(angle),zz))
 faces=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);return o
for i,cx in enumerate([-.96,0,.96]):
 for j in range(8):
  a=j*math.tau/8;diamond('Flower %d / petal %d'%(i,j),cx+.225*math.cos(a),.225*math.sin(a),.155,.075,2.012,red if j%2==0 else ivory,a)
 diamond('Flower %d / heart'%i,cx,0,.08,.08,2.020,gold)
 for sy in [-1,1]:
  diamond('Flower %d / leaf'%i,cx,sy*.55,.16,.075,2.008,green,.4*sy)
'''
tail=s[s.index('# Medallion is solid'):]
tail=tail.replace('japan.blend','moldova.blend').replace('japan.glb','moldova.glb').replace('JAPAN AUTHORED','MOLDOVA AUTHORED')
tail=tail.replace('scene.cycles.samples=32','scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=1000').replace('resolution_y=1000','resolution_y=900')
(R/'author.py').write_text(head+materials+utils+body+tail)
