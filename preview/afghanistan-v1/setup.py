from pathlib import Path
import shutil
R=Path(__file__).resolve().parent;S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copy2(S/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','viewer.js','template.html','verify_browser.py','package.json']:
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','afghanistan-v1').replace('japan.glb','afghanistan.glb').replace('japan.blend','afghanistan.blend').replace('Japan / Cedar & Moss','Afghanistan / Lapis & Hindu Kush').replace('Japan Cedar and Moss','Afghanistan Lapis and Hindu Kush').replace('Yakushima cedar. Mossed granite. Quiet brass.','Badakhshan blue. Mineral veins. Mountain relief.').replace('the original Japan concept','a researched Afghan lapis and mountain brief').replace('JAPAN ·','AFGHANISTAN ·')
 if name=='build.py':s=s.replace("['node',", "['C:/Program Files/nodejs/node.exe',")
 if name=='template.html':
  s=s.replace('font-siz... [truncated]','font-size:30px}.foot{flex-direction:column}.folio{white-space:normal}}')
 if name=='viewer.js':
  s=s.replace("target=target?0:1;open.textContent", "target=target?0:1;if(reduced.matches){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;window.pilot.lid=p.lid;window.pilot.latch=p.latch;}open.textContent")
  s=s.replace("controls.reset();open.textContent", "controls.reset();lid.rotation.x=latch.rotation.x=0;window.pilot.progress=0;window.pilot.lid=window.pilot.latch=0;open.textContent")
 (R/name).write_text(s,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
s=(S/'author.py').read_text()
s=s[:s.index("wood=mat")]+'''wood=mat('Lapis / calcite and pyrite',(.025,.07,.28),.32);maptex(wood,'lapis-color.png','Base Color');maptex(wood,'lapis-roughness.png','Roughness',True)
t=wood.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/lapis-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=wood.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.22;wood.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);wood.node_tree.links.new(n.outputs['Normal'],wood.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
granite=mat('Mountain / pale marble',(.42,.39,.32),.83);maptex(granite,'marble.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / deep blue',(.013,.025,.06),.8)
''' +s[s.index('def uv('):]
a=s.index("   u=co.y");b=s.index('def cube(',a)
s=s[:a]+'''   normal=p.normal
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/2.4+.5,v/2.4+.5)
'''+s[b:]
a=s.index('# Exterior skins');b=s.index('# Small collar',a)
s=s[:a]+'''# Continuous lapis skins with nonoverlapping corner joins.
for sy in [-1,1]:cube('Lapis / front' if sy<0 else 'Lapis / rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.012)
for sx in [-1,1]:cube('Lapis / side',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.012)
'''+s[b:]
a=s.index('# A thin satin');b=s.index('# Restrained brass',a);s=s[:a]+s[b:]
a=s.index("stone('Terrain / granite'");b=s.index('# Medallion',a)
s=s[:a]+'''# Continuous closed-sided three-peak mountain relief, not surveyed topography.
verts=[];faces=[];nx=49;ny=25
for j in range(ny):
 y=-.64+1.28*j/(ny-1)
 for i in range(nx):
  x=-1.30+2.60*i/(nx-1)
  env=max(0,math.sin(math.pi*i/(nx-1))*math.sin(math.pi*j/(ny-1)))**.7
  peaks=max(.47*math.exp(-((x+.78)/.26)**2-((y-.10)/.30)**2),.64*math.exp(-((x+.02)/.30)**2-((y-.02)/.36)**2),.52*math.exp(-((x-.76)/.27)**2-((y-.17)/.31)**2))
  z=1.978+env*(.045+peaks+.022*math.sin(x*31+y*17)*math.sin(y*23))
  verts.append((x,y,z))
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;faces.extend([(a,a+1,a+nx+1),(a,a+nx+1,a+nx)])
edge=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(range(nx*ny-2,nx*(ny-1)-1,-1))+[j*nx for j in range(ny-2,0,-1)]
bot=[]
for k in edge:bot.append(len(verts));verts.append((verts[k][0],verts[k][1],1.970))
for k in range(len(edge)):
 q=(k+1)%len(edge);faces.append((edge[k],bot[k],bot[q],edge[q]))
faces.append(tuple(reversed(bot)))
me=bpy.data.meshes.new('Hindu Kush relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Hindu Kush three peaks',me);bpy.context.collection.objects.link(o);me.materials.append(granite);uv(o);parent(o)
'''+s[b:]
s=s.replace('Cedar /','Lapis /').replace('Granite foot','Marble foot').replace('japan.blend','afghanistan.blend').replace('japan.glb','afghanistan.glb').replace('JAPAN AUTHORED','AFGHANISTAN AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=2;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=720')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Prepared additive source and mechanics')
