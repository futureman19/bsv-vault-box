"""Build local author from disclosed Japan helper lineage; run once in repository."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
header=s[s.index('import bpy'):s.index("wood=mat")]
materials="""wood=mat('Earth / terracotta sediment',(.55,.28,.12),.8);maptex(wood,'earth-color.png','Base Color');maptex(wood,'earth-roughness.png','Roughness',True)
granite=mat('Earth / dark erosion',(.25,.12,.06),.85);maptex(granite,'dark-earth.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Earth / dark seam',(.07,.035,.018),.9)
"""
helpers=s[s.index('def uv('):s.index('# Exterior skins')]
body="""for sy in [-1,1]:cube('Sediment / front rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Sediment / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025,axis='Y')
cube('Sediment / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Earth seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.09),seam,bevel=.009)
for sx in [-1,1]:cube('Earth seam / side',(sx*1.74,0,1.618),(.16,2.05,.09),seam,bevel=.009)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
"""
hardware=s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]
terrain="""# Three asymmetric eroded cliff ribbons, sculpted as triangulated heightfields.
# Continuous bases touch the lid, gully modulation has actual geometric depth.
for k,(cx,cy,w,d,h) in enumerate([(-.94,.35,.86,.9,.47),(0,.47,.87,1.0,.60),(.9,.38,.74,.9,.50)]):
 verts=[];faces=[];nx=25;ny=19
 for j in range(ny):
  for i in range(nx):
   u=i/(nx-1);v=j/(ny-1);xx=cx+(u-.5)*w;yy=cy+(v-.5)*d
   edge=math.sin(math.pi*u)**.65*math.sin(math.pi*v)**.65
   gullies=.62+.22*math.sin(u*math.tau*4+v*2+k)+.12*math.sin(u*math.tau*9-v*3)
   z=1.979+h*edge*gullies*(.7+.3*v)
   verts.append((xx,yy,z))
 for j in range(ny-1):
  for i in range(nx-1):
   a=j*nx+i;faces.extend([(a,a+1,a+nx+1),(a,a+nx+1,a+nx)])
 me=bpy.data.meshes.new('Eroded cliff');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Cliff / eroded buttress '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
"""
tail=s[s.index('# Medallion is solid'):].replace('japan.blend','angola.blend').replace('japan.glb','angola.glb').replace('JAPAN AUTHORED','ANGOLA AUTHORED')
(R/'author.py').write_text('"""Angola Miradouro da Lua; procedural source, adapted Japan mechanism helpers."""\n'+header+materials+helpers+body+hardware+terrain+tail)
print('AUTHOR PREPARED')
