"""Create this pilot's author from the read-only mechanical helper lineage."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
start=s[:s.index('wood=mat(')]
helpers=s[s.index('def cube('):s.index('for o in bpy.data.objects:')]
uv='''def uv(o,axis='X'):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar projection')
 for p in o.data.polygons:
  a=max(range(3),key=lambda i:abs(p.normal[i]));axes=[i for i in range(3) if i!=a]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.6,co[axes[1]]*.6)
'''
materials='''sand=mat('Limestone / fine sand pores',(.65,.45,.25),.72)
maptex(sand,'sand-color.png','Base Color');maptex(sand,'sand-roughness.png','Roughness',True)
t=sand.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/sand-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack()
n=sand.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.22;sand.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);sand.node_tree.links.new(n.outputs['Normal'],sand.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / champagne',(.55,.37,.16),.27,.8)
water=mat('Tidal water / turquoise',(.018,.31,.34),.23,.12)
seam=mat('Seam / dark teal',(.015,.047,.043),.85)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(sand if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),sand,bevel=.02)
for sx in [-1,1]:cube('Limestone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),sand,bevel=.02)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),sand,bevel=.025)
for sy in [-1,1]:cube('Tidal seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Tidal seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),sand,bevel=.004)
  cube('Limestone / foot',(sx*1.47,sy*.91,-.10),(.54,.46,.34),sand,bevel=.08)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),sand,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def mesh(n,verts,faces,material):
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o)
 for p in me.polygons:p.use_smooth=True
 return o
# Three solid curved sand ridges with narrow crests and asymmetrical slopes.
for k,(cx,cy,length,width,height) in enumerate([(-.10,.62,2.5,.58,.38),(-.35,-.57,2.1,.49,.24),(.93,-.10,1.2,.40,.19)]):
 vs=[];fs=[];nu=48;nv=16
 for i in range(nu+1):
  u=i/nu;xx=cx+(u-.5)*length;curve=cy+.09*math.sin(u*math.pi*1.5+k)
  envelope=max(0,math.sin(math.pi*u))**.65
  for j in range(nv+1):
   v=j/nv;crest=.62;profile=(v/crest if v<crest else (1-v)/(1-crest))
   vs.append((xx,curve+(v-.5)*width,1.975+.045+height*envelope*max(0,profile)**.8))
 for i in range(nu):
  for j in range(nv):a=i*(nv+1)+j;fs.append((a,a+nv+1,a+nv+2,a+1))
 boundary=list(range(nv+1))+[i*(nv+1)+nv for i in range(1,nu+1)]+[nu*(nv+1)+j for j in range(nv-1,-1,-1)]+[i*(nv+1) for i in range(nu-1,0,-1)]
 for j,a in enumerate(boundary):
  b=boundary[(j+1)%len(boundary)];q=len(vs);vs.extend([(vs[a][0],vs[a][1],1.97),(vs[b][0],vs[b][1],1.97)]);fs.append((a,q,q+1,b))
 mesh('Dune / curved ridge '+str(k),vs,fs,sand)
# Narrow tidal ribbon through the central negative space, not a rectangular plaque.
vs=[];fs=[]
for i in range(65):
 u=i/64;x=-1.45+u*2.85;y=.04+.10*math.sin(u*math.tau);w=.27+.18*math.sin(math.pi*u)**2
 vs.extend([(x,y-w/2,1.992),(x,y+w/2,1.992)])
for i in range(64):a=2*i;fs.append((a,a+2,a+3,a+1))
mesh('Tidal inlet / continuous blue ribbon',vs,fs,water)
'''
end=s[s.index('# Medallion is solid'):].replace("'japan.blend'","'qatar.blend'").replace("'japan.glb'","'qatar.glb'").replace('JAPAN AUTHORED','QATAR AUTHORED').replace("scene.cycles.samples=32","scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4").replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.6)')
(R/'author.py').write_text(start+uv+helpers+materials+end)
print('AUTHOR WRITTEN')
