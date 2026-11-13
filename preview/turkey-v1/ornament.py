# Three raised original tulip silhouettes, not copied museum motifs.
def relief(name,xy,material):
 n=len(xy);verts=[(x,y,z) for z in [2.006,2.065] for x,y in xy]
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);return o
for i,x in enumerate([-.92,0,.92]):
 top=.30 if i!=1 else .55
 pts=[(x-.04,-.68,2.018),(x-.12,-.34,2.018),(x+.03,-.05,2.018),(x,top-.18,2.018)]
 tube('Ornament / stem '+str(i),pts,[.019]*4,green,sides=8)
 shape=[(-.17,-.12),(-.26,.18),(-.10,.10),(0,.31),(.10,.10),(.26,.18),(.17,-.12),(0,-.22)]
 relief('Ornament / tulip '+str(i),[(x+a,top+b) for a,b in shape],red)
 for side in [-1,1]:
  relief('Ornament / leaf '+str(i)+' '+str(side),[(x,-.25),(x+side*.30,-.05),(x+side*.21,-.41),(x,-.46)],green)
# Cobalt beaded border is co-moving with the ceramic panel.
for sy in [-1,1]:
 for j in range(23):
  x=-1.43+j*2.86/22
  bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=1,location=(x,sy*.82,2.018));o=bpy.context.object;o.name='Ornament / cobalt border';o.scale=(.026,.026,.012);o.data.materials.append(blue);parent(o)
