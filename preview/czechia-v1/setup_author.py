from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('wood=mat')]+'''wood=mat('Cobalt / polished glass inspired enamel',(.02,.08,.25),.22);maptex(wood,'cobalt.png','Base Color');maptex(wood,'roughness.png','Roughness',True)
end=wood
granite=mat('Blue gray stone',(.12,.18,.23),.7);maptex(granite,'stone.png','Base Color')
gold=mat('Brass / satin',(.48,.30,.10),.28,.8)
seam=mat('Dark blue seam',(.012,.022,.045),.8)
crystal=mat('Pale blue cut glass inspired ornament',(.32,.63,.82),.16,.22)
'''+s[s.index('def uv('):s.index('# Exterior skins')]+'''# Continuous cobalt shell, butt-joined corners.
for sy in [-1,1]:cube('Cobalt / front rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.008)
for sx in [-1,1]:cube('Cobalt / sides',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.008,axis='Y')
'''+s[s.index('# Small collar'):s.index('# A thin satin')]+s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]+'''# Cut-glass rosette: concentric staggered rings create true triangular facets.
def gem(n,x,y,r,h):
 verts=[(x,y,1.98)]
 for rad,z,offset in [(r,2.015,0),(r*.72,2.015+h*.65,math.pi/12),(r*.30,2.015+h,0)]:
  for j in range(12):
   a=j*math.tau/12+offset;verts.append((x+rad*math.cos(a),y+rad*math.sin(a),z))
 verts.append((x,y,2.015+h+.025));faces=[]
 for j in range(12):
  k=(j+1)%12;faces.append((0,1+k,1+j))
  for start in [1,13]:faces.extend([(start+j,start+k,start+12+j),(start+k,start+12+k,start+12+j)])
  faces.append((25+j,25+k,37))
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(crystal);parent(o)
gem('Cut crystal / central rosette',0,0,.66,.48)
for j in range(8):
 a=j*math.tau/8;gem('Cut crystal / satellite '+str(j),1.18*math.cos(a),.67*math.sin(a),.19,.17)
'''+s[s.index('# Medallion'):]
s=s.replace('japan.blend','czechia.blend').replace('japan.glb','czechia.glb').replace('JAPAN AUTHORED','CZECHIA AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=800')
(R/'author.py').write_text(s)
