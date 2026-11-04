"""Create Sweden author from the read-only Japan mechanical construction scaffold."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s.replace('Reference-led Japan pilot','Brief-led Sweden pilot').replace('japan.blend','sweden.blend').replace('japan.glb','sweden.glb').replace('JAPAN AUTHORED','SWEDEN AUTHORED')
s=s.replace("wood=mat('Cedar / fine longitudinal grain'", "wood=mat('Falun red / painted wood'").replace('cedar-color.png','red-color.png').replace('cedar-roughness.png','wood-roughness.png').replace('cedar-end.png','wood-end.png')
s=s.replace("end=mat('Cedar / dark finger endgrain'", "end=mat('Pine / exposed endgrain'")
s=s.replace("granite=mat('Granite / salt and pepper',(.24,.25,.25),.85);maptex(granite,'granite.png','Base Color')", "granite=mat('Dark wooden feet',(.065,.030,.015),.72)\ninner=mat('Pine / pale interior',(.60,.43,.23),.65);maptex(inner,'wood-end.png','Base Color')\nblue=mat('Kurbits / blue ground',(.025,.085,.18),.48)\ncream=mat('Kurbits / warm ivory',(.83,.67,.40),.5)\ngreen=mat('Kurbits / leaf green',(.052,.13,.050),.6)")
s=s.replace("wood if o.name.startswith('Interior') else gold", "inner if o.name.startswith('Interior') else gold")
s=s.replace("(.035,.07,.032)","(.028,.018,.012)")
a=s.index("for sx in [-1,1]:\n for sy in [-1,1]:stone('Granite foot'")
b=s.index('def tube(',a)
s=s[:a]+"for sx in [-1,1]:\n for sy in [-1,1]:cube('Dark wood foot',(sx*1.47,sy*.91,-.10),(.46,.40,.30),granite,bevel=.045)\n"+s[b:]
a=s.index('trunk=[');b=s.index('# Medallion',a)
s=s[:a]+'''# Invented kurbits-inspired relief, not a historical motif reproduction.
cube('Kurbits / blue inset',(0,0,2.00),(3.10,1.72,.060),blue,lid,.015)
def leaf(n,x,y,angle,scale,material):
 # Closed lenticular prism with a gently raised central ridge.
 verts=[(-scale,0,0),(0,-scale*.38,0),(scale,0,0),(0,scale*.38,0),(0,0,.028)]
 verts=[(x+u*math.cos(angle)-v*math.sin(angle),y+u*math.sin(angle)+v*math.cos(angle),2.026+z) for u,v,z in verts]
 faces=[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)]
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o)
for side in [-1,1]:
 points=[(0,-.62,2.054),(side*.28,-.36,2.054),(side*.56,-.02,2.054),(side*.86,.25,2.054),(side*1.12,.37,2.054)]
 tube('Kurbits / curling stem',points,[.025]*5,cream,sides=8)
 for j in range(5):
  x=side*(.22+j*.18);y=-.37+j*.15
  leaf('Kurbits / green leaf',x,y+.14,side*1.0,.16,green)
  leaf('Kurbits / ivory leaf',x+.06*side,y-.12,side*-.65,.13,cream)
for cx,cy,r in [(0,.34,.25),(-1.12,.39,.18),(1.12,.39,.18)]:
 for j in range(8):
  a=j*math.tau/8
  leaf('Kurbits / flower petal',cx+math.cos(a)*r*.60,cy+math.sin(a)*r*.60,a,r*.57,cream)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=(cx,cy,2.064));o=bpy.context.object;o.name='Kurbits / red flower heart';o.scale=(r*.40,r*.40,.035);o.data.materials.append(wood);uv(o);parent(o)
tube('Kurbits / central stem',[(0,-.62,2.054),(0,-.2,2.054),(0,.34,2.054)],[.024]*3,cream,sides=8)
''' +s[b:]
s=s.replace("scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=900;scene.render.resolution_y=820")
s=s.replace("Cedar /", "Red wood /").replace("Mineral seam / moss green","Dark seam")
(R/'author.py').write_text(s,encoding='utf8')
print('Created author.py from scoped source scaffold')
