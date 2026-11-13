# Executed in author.py after body creation. All coordinates are source world.
lightwood=mat('Carved timber / golden endgrain',(.62,.38,.16),.62)
roofmat=mat('Weathered shingle / smoked timber',(.105,.068,.042),.76)
# Framed diamond inlays sit just above the lid; front and rear are deliberately
# inset from the family hardware. Invented decoration, not copied folk symbols.
for sy in [-1,1]:
 for x in [-1.35,-.90,-.45,0,.45,.90,1.35]:
  y=sy*.87
  for dx,dy,angle in [(-.065,0,math.pi/4),(.065,0,-math.pi/4)]:
   for flip in [-1,1]:
    o=cube('Border diamond / inlay',(x+dx,y+flip*.065,1.994),(.18,.022,.018),lightwood,lid,0)
    o.rotation_euler.z=angle*flip
for sy in [-1,1]:cube('Border / rail',(0,sy*1.025,1.995),(3.22,.025,.024),lightwood,lid,.003)
# Secular abstract timber roof, modeled as a solid triangular prism.
def mesh(n,verts,faces,material):
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
cube('Roof / timber foundation',(-.18,.02,2.06),(1.98,.90,.16),wood,lid,.012)
verts=[(x,y,z) for x in [-1.20,.84] for y,z in [(-.50,2.13),(.54,2.13),(.02,2.62)]]
mesh('Roof / double slope core',verts,[(0,2,1),(3,4,5),(0,3,5,2),(2,5,4,1),(1,4,3,0)],roofmat)
# Small individually modeled shingle plates in staggered rows. Bottom faces are
# seated in the roof; ridge is continuous rather than floating tiles.
for side in [-1,1]:
 for row in range(5):
  t=(row+.5)/5;y=.02+side*(.52*(1-t));z=2.13+.49*t+.012
  for col in range(10):
   x=-1.20+(col+.5)*.204
   o=cube('Roof shingle / row %d tile %d'%(row,col),(x,y,z),(.197,.151,.023),roofmat,lid,.003)
   o.rotation_euler.x=-side*math.atan2(.49,.52)
cube('Roof / ridge cap',(-.18,.02,2.638),(2.10,.065,.055),lightwood,lid,.01)
# Slim wooden spire at the right rear, abstracted without cross or icon.
cube('Spire / timber shaft',(.98,.38,2.38),(.27,.27,.78),wood,lid,.012)
cube('Spire / collar',(.98,.38,2.76),(.36,.36,.075),lightwood,lid,.008)
verts=[(.98+dx,.38+dy,2.79) for dx,dy in [(-.23,-.23),(.23,-.23),(.23,.23),(-.23,.23)]]+[(.98,.38,3.10)]
mesh('Spire / steep four sided cap',verts,[(3,2,1,0),(0,1,4),(1,2,4),(2,3,4),(3,0,4)],roofmat)
