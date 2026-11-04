from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt'] : shutil.copy2(S/n,R/n)
for n in ['build.py','viewer.js','motion.mjs','verify_source.py','verify_parity.py','verify_browser.py','package.json','template.html']:
 s=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','hungary-v1').replace('japan','hungary').replace('Japan','Hungary').replace('JAPAN','HUNGARY').replace('Cedar & Moss','Pécs Lustre').replace('Cedar and Moss','Pécs Lustre').replace('Yakushima cedar. Mossed granite. Quiet brass.','Jade ceramic. Golden flowers. Pécs-inspired lustre.').replace('inspired by the original Hungary concept','inspired by Hungarian decorative ceramics')
 s=s.replace('h1{font-siz... [truncated]','h1{font-size:32px}.foot{flex-direction:column}.folio{display:none}}')
 (R/n).write_text(s,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
s=(S/'author.py').read_text(encoding='utf8')
# Keep mechanism and utility definitions, not Japanese geometry.
out=s[:s.index("wood=mat")]
out+='''wood=mat('Ceramic / jade lustre',(.04,.22,.12),.28,.5);maptex(wood,'jade.png','Base Color');maptex(wood,'roughness.png','Roughness',True)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
ivory=mat('Ceramic / ivory glaze',(.8,.72,.49),.3);maptex(ivory,'ivory.png','Base Color')
seam=mat('Seam / dark jade',(.015,.035,.025),.8)
'''
out+=s[s.index('def uv('):s.index('# Exterior skins')]
out+='''for sy in [-1,1]:cube('Ceramic / front-rear skin',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.018)
for sx in [-1,1]:cube('Ceramic / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.018,axis='Y')
'''
out+=s[s.index('# Small collar'):s.index('# A thin satin')].replace('Cedar /','Ceramic /')
out+=s[s.index('# Restrained brass'):s.index('def stone(')]
out+='''for sx in [-1,1]:
 for sy in [-1,1]:cube('Ceramic foot',(sx*1.47,sy*.91,-.09),(.46,.4,.30),ivory,bevel=.07)
'''
out+=s[s.index('def tube('):s.index('trunk=[')]
out+='''def petal(n,loc,scale,angle,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:v.co=Vector((v.co.x*scale[0],v.co.y*scale[1],v.co.z*scale[2]))
 o.rotation_euler.z=angle;o.data.materials.append(material)
 for f in o.data.polygons:f.use_smooth=True
 parent(o);return o
centers=[(0,0),(-.98,-.55),(.98,-.55),(-.98,.55),(.98,.55)]
for k,(x,y) in enumerate(centers):
 petal('Rosette center / '+str(k),(x,y,2.065),(.085,.085,.06),0,gold)
 for j in range(8):
  a=j*math.tau/8;petal('Petal / '+str(k)+'-'+str(j),(x+.145*math.cos(a),y+.145*math.sin(a),2.04),(.155,.064,.055),a,ivory if j%2 else gold)
for k,(x,y) in enumerate(centers[1:]):
 pts=[(x*t,y*t+.12*math.sin(t*math.pi)*(1 if y>0 else -1),2.004) for t in [i/12 for i in range(13)]]
 tube('Floral stem / '+str(k),pts,[.018]*len(pts),gold)
 for j,t in enumerate([.40,.65]):
  petal('Leaf / '+str(k)+'-'+str(j),(x*t,y*t+.12*math.sin(t*math.pi)*(1 if y>0 else -1),2.025),(.16,.065,.037),math.atan2(y,x)+(0.6 if j else -.6),wood)
'''
out+=s[s.index('# Medallion'):]
out=out.replace('japan','hungary').replace('JAPAN','HUNGARY').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(out,encoding='utf8')
print('Scoped setup complete')
